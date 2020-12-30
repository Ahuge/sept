# Problem:
We need an easy to use, obvious folder structure template tool that will allow non technical users to modify it.
It needs full control for client naming specifications while at the same time being easy to implement and understand.

# Solution:
After reading up on existing templating languages, I am proposing a new templating language that defines a concept of Operators and Tokens.

## Operators
Operators are essentially functions working on Tokens.
The provided list of Operators is small however technical clients will be able to expose additional Operators by [extending the system](#extending-the-system).

## Tokens
Tokens are inputs mapped from a Version entity in Shotgun.
Clients can provide custom Tokens by [extending the system](#extending-the-system) and returning a map of {Version.field: Token.name}.


## Template Configuration File
The template configuration file will contain the following yaml keys  
```
  FramesTemplate
  MovieTemplate
  [Custom Operators Function] - Optional? Falls back to hook?
  [Custom Tokens Function]    - Optional? Falls back to hook?
```

## Extending The System
The templating system allows defining custom Operators via registration callbacks. In our implementation we will pass client provided Operators to the library.  
The templating system expects a token schema to be fully realized before implementing a parser.  
In our case, we want to allow the client to provide custom Tokens from a Version entity.  
We do this by by allowing the client code to provide us a mapping of Version entity fields to Token names.


# Token Syntax
A Token starts with a double curly brace, an optional Operator and then a Token name and is closed with a double curly brace.
In practice it looks like the following: `{{(<Operator>)?: <Token>}}`

# Operator Syntax
An Operator can optionally expose args and they get passed in via square braces.
In practice the schema looks like the following: `<Operator>([args])?`

# Expression Examples:
```
  {{Shot}}               - Token, no Operator
  {{lower: Shot}}        - Token with a basic Operator
  {{upper: Shot}}        - Token with a basic Operator
  {{substr[0,4]: Shot}}  - Token with an Operator requiring args
```


# Built-in Operator list:
```
  lower
    Args: None
    Description: Makes the entire Token lower case

  upper
    Args: None
    Description: Makes the entire Token upper case

  substr
    Args: int Start, int End
    Description: Grabs a subset of the Token.
```

# Default Tokens
In our Shotgun framework, we provide the following default Tokens:
```
shot.Shot.code.           - Shot
task.Task.code            - Task
sg_sequence.Sequence.code - Sequence
<Unknown>                 - Episode
project.name              - Project
created_by.HumanUser.name - Artist
created_at                - Date (Version entity created)
```
