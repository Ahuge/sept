# Simple Extensible Path Template
[![SEPT Version](https://img.shields.io/pypi/v/sept.svg)](https://pypi.org/project/sept) [![SEPT Downloads](https://img.shields.io/pypi/dm/sept.svg)](https://pypi.org/project/sept) [![SEPT Supported Python Versions](https://img.shields.io/pypi/pyversions/sept.svg)](https://pypi.org/project/sept) [![Documentation Status](https://readthedocs.org/projects/sept/badge/?version=latest)](https://sept.readthedocs.io/en/latest/?badge=latest)

The Simple Extensible Path Template (sept) is a simple to use, simple to configure templating system designed for you!

If you are a developer, SEPT can help you put the power back into the hands of your users.  
If you are an artist, producer, or editor, you can use SEPT to control naming of thousands of files automatically in a consistent way!  
  
  
We have written a "Getting Started" Tutorial for [Users](https://sept.readthedocs.io/en/latest/introduction/non-developer.html) and for [Developers](https://sept.readthedocs.io/en/latest/introduction/developer.html) which will get you up and running with SEPT quickly.  

<br>
We also support a "live" tutorial thanks to [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb).  
The [User](https://colab.research.google.com/github/Ahuge/sept/blob/release/docs/introduction/non-developer.ipynb) tutorial and the [Developer](https://colab.research.google.com/github/Ahuge/sept/blob/release/docs/introduction/developer.ipynb)

<br>
<br>
The rest of this document will give you a quick look at SEPT templates and some examples. This may be to abrupt of a jump for you and I would recommend viewing the "Getting Started" tutorials first.  

## Table Of Contents
- [Examples](#examples)
  - [Hello World](#hello-world-example)
  - [Custom Tokens](#a-slightly-more-complex-example)
  - [Nested Operators](#nested-operators)
  - [Operators Arguments](#passing-arguments-to-operators)
  - [Custom Operators](#custom-operators)

- [Provided Operators](#provided-operators)
  - [lower](#loweroperator)
  - [upper](#upperoperator)
  - [substr](#substroperator)
  - [replace](#replaceoperator)
  - [datefmt](#todo-datefmtoperator)

# Examples
## Hello World Example
There is some test coverage which can operate as simple examples that may go beyond this example.
```python
from sept import PathTemplateParser
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
from sept import PathTemplateParser, Token
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
from sept import PathTemplateParser, Token
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
In `sept` Operators can accept arguments and they are defined within square brackets, comma delimited.


## Custom Operators
```python
import six

from sept import PathTemplateParser, Operator
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

# Contributing
Contributions are encouraged!
If you have a large code refactor or a significant change, starting an issue to discuss the change and plan is recommended.
If you want to help with documentation, that is somewhere that we also need more work on as well.
