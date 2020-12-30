# Path Template
Path Template is a simple to configure templating system designed at relatively simple path translation or path generation from a dictionary of data.  

Client code can define a set of Tokens that are in the dictionary of data by creating a subclass of `path_template.Token`.  
Advanced users have the ability to define custom Operators that can modify the data in the dictionary.  

# Design Goals
Path Template is designed with non technical editors in mind. These people use computers but have very limited (if at all) experience with programming.  

The goal isn't to allow for arbitrary code run from the template. The default Operator subset is small for a reason, if there are advanced use cases you need, consider implementing them yourself if they are too large in scope.  

We also want useful error messages. Providing errors with character numbers when templates cannot be parsed for example.    

I want this system to be extensible, allow client code to provide custom Operators or Tokens as needed.   

Speed is not a design goal currently, this is python, if you are doing large scale templating, there are more complex libraries for that.


# Contributing
Contributions are encouraged!  
If you have a large code refactor or a significant change, starting an issue to discuss the change and plan is recommended.  
If you want to help with documentation, that is somewhere that we also need more work on as well.  

# Examples
## Hello World Example
There is some test coverage which can operate as simple examples that may go beyond this example.  
```python
from path_template import PathTemplateParser
data = {
  "first": "Alex",
  "last": "Hughes",
}

template_str = "/home/{{lower: first}}"
parser = PathTemplateParser()

template = parser.validate_template(template_str)
resolved_path = template.resolve(data)
# /home/alex
```
In the above example, we are executing the `lower` Operator on the `first` Token.  
Now, we haven't defined a `first` token but because `first` matches exactly to a top level value in the `data`, it gets resolved automatically for us.  
The `lower` Operator is quite simple and performs a `str.lower()` operation on the value that our Token returns, in this case "Alex" is given to the `lower` Operator.  

## A slightly more complex example
In this example, we don't have a top level key that matches exactly, we have to define a custom Token that will dig deep into our data dictionary and pull out the value we want.  
```python
from path_template import PathTemplateParser, Token
data = {
  "user": {
    "HumanUser": {
      "first": "Alex",
      "last": "Hughes",
    },
  },
}

class FirstNameToken(Token):
    name = "first"
    def getValue(self, data):
        return data.get("user", {}).get("HumanUser", {}).get("first")


template_str = "/home/{{lower: first}}{{upper: first}}"
parser = PathTemplateParser(additional_tokens=[FirstNameToken])

template = parser.validate_template(template_str)
resolved_path = template.resolve(data)
# /home/alexALEX
```
As you can see above, we had to pass an additional keyword argument to the `PathTemplateParser` class.  
This argument, and the corresponding Operator one, expect a list of python class objects inheriting from Token or Operator.  

This is also the first example where we have multiple expressions in it.  


## Nested Operators
It is possible to nest multiple Operators against a single Token.  
The thing to remember in this case is that Tokens are resolved inside out.  
```python
from path_template import PathTemplateParser, Token
data = {
  "first": "Alex",
  "last": "Hughes",
}


template_str = "/home/{{substr[0, 1]: {{lower: first}}}}{{lower: last}}"
parser = PathTemplateParser()

template = parser.validate_template(template_str)
resolved_path = template.resolve(data)
# /home/ahughes
```
In the above example, we have two main expressions,
`{{substr[0, 1]: {{lower: first}}}}` and `{{lower: last}}`.  
Ignore the syntax of the `substr` Operator for now and take a look at the nested `lower` + `first` expression.  
The way this gets resolved is by first calling `lower` on the `first` Token and then passing the result of that Operator, to the `substr` Operator.  

## Passing Arguments to Operators
In the previous example I told you to ignore the `{{substr[0, 1]: ...}}` syntax you saw.  
That was us passing arguments to the `substr` Operator.  In the case above, we passed 2 values, 0 and 1.  
In `path_template` Operators can accept arguments and they are defined within square brackets, comma delimited.   


## Custom Operators
```python
import six

from path_template import PathTemplateParser, Operator
data = {
  "first": "Alex",
  "last": "Hughes",
}

class ReverseOperator(Operator):
    name = "reverse"
    DATA_TYPES = (six.text_type, six.binary_type)
    def is_invalid(self, token_value):
        if isinstance(token_value, self.DATA_TYPES):
            # Is valid
            return None
        elif not token_value:
            # Value is empty
            return "Missing text value"
        return "Value must be one of the following data types ({})".format(
            self.DATA_TYPES
        )

    def execute(self, input_data):
        output_data = ""
        for char in reversed(input_data):
            output_data += char
        return output_data


template_str = "/home/{{reverse: last}}"
parser = PathTemplateParser(additional_operators=[ReverseOperator])

template = parser.validate_template(template_str)
resolved_path = template.resolve(data)
# /home/sehguh
```
This is very similar to our Token example, the Operator schema is two functions.  
```python
def is_invalid(self, token_value):
    """
    is_invalid will check the value the is about to be operated on.
    If the value will not work for some reason (wrong datatype, etc),
        this method should return an error message as a string.
    
    If it looks good to go, just return None
    
    :param Any token_value: Data that would be operated on
    :return: A Falsey value if everything is ok, or an error string if not.
    :rtype: None|str
    """

def execute(self, input_data):
    """
    execute does the actual work of your custom Operator.
    It will take in the data passed and return the transformed data as
        output.

    :param Any input_data:
    :return: The transformed data according to whatever the Operator is
        supposed to do.
    :rtype: Any
    """
```

# Provided Operators
## LowerOperator
The `lower` Operator will transform the passed text to lowercase.  
It takes no arguments.  

## UpperOperator
The `upper` Operator will transform the passed text to uppercase.  
It takes no arguments

## SubStrOperator
The `substr` Operator will return a subset of the text passed to it.  
It takes 1 or 2 arguments, `start` and `end` respectively.  
It also supports the "start" and "end" keywords. This may be easier than teaching a non-technical person that indexes start at 0.  


## [TODO] DateFmtOperator
The `datefmt` Operator will return a date with custom formatting.  
It takes 1 argument that is the "date formatting".  
You should pass a string like the following: `{{datefmt[YY-MM-DD]: created_at}}`.  

### DateFmt Formatting Options
```markdown
YY        - Year last two numbers (2021 becomes 21)
YYYY      - Year four numbers (2021 becomes 2021)
M         - Month as one or two numbers (two only if needed, ie 11)
MM        - Month as two numbers (3 becomes 03)
D         - Day as one or two numbers (two only if needed, ie 11)
DD        - Day as two numbers (3 becomes 03)
H         - Hour as one or two numbers 24hr time (two only if needed, ie 11)
HH        - Hour as two numbers 24hr time (3 becomes 03)
m         - Minute as one or two numbers (two only if needed, ie 11)
mm        - Minute as two numbers (3 becomes 03)
s         - Second as one or two numbers (two only if needed, ie 11)
ss        - Second as two numbers (3 becomes 03)
``` 