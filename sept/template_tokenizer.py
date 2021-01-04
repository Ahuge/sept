import pyparsing

token_group_start = pyparsing.Literal("{{")
token_group_end = pyparsing.Literal("}}")
escaped_character = "\\" + pyparsing.alphanums

operator_name = pyparsing.Word(pyparsing.alphanums)("Operator")
operator_args = pyparsing.delimitedList(
    pyparsing.OneOrMore(
        pyparsing.Word(pyparsing.printables, escaped_character, excludeChars="[],")
    )
)("Args")

operator_arg_group = pyparsing.Literal("[") + operator_args + pyparsing.Literal("]")

operator = (
    operator_name
    + pyparsing.Optional(
        operator_arg_group,
    )
    + pyparsing.Literal(":")
)
token_name = pyparsing.Word(pyparsing.printables, excludeChars="{}[]:")("Token")


class Node(object):
    def __init__(self, Operator, Args, Token, length, tok_start, tok_str, child=()):
        super(Node, self).__init__()
        self.Operator = Operator
        self.Args = Args
        self.Token = Token
        self.child = child
        self.length = length
        self.start = int(tok_start)
        self.end = int(tok_start + self.length)
        self.original_str = tok_str

    def __len__(self):
        return self.length

    def __repr__(self):
        msg = "<Node "
        if self.Operator:
            msg += "Operator:{} ".format(self.Operator)
        if self.Args:
            msg += "Args:{} ".format(self.Args)
        if self.Token:
            msg += "Token:{}".format(self.Token)
        elif self.child:
            msg += "Child:{}".format(self.child)
        msg += ">"
        return msg


def parseAction(string, location, tokens):
    operator = tokens.Operator
    operator_args = tokens.Args
    token = tokens.Token or tokens[-2]
    length = sum(map(len, filter(lambda t: t is not None, tokens)))

    if operator_args:
        # We add n-1 length to handle the commas
        length += len(operator_args) - 1
    end = location + length
    if isinstance(token, Node):
        new_node = Node(
            child=token,
            Operator=operator,
            Args=operator_args,
            Token=None,
            length=length,
            tok_start=location,
            tok_str=string[location:end],
        )
    else:
        new_node = Node(
            child=None,
            Operator=operator,
            Args=operator_args,
            Token=token,
            length=length,
            tok_start=location,
            tok_str=string[location:end],
        )
    return new_node


Tokenizer = pyparsing.Forward().setResultsName("match")

Tokenizer << (
    token_group_start
    + pyparsing.Optional(operator, default=None)
    + (Tokenizer | token_name)
    + token_group_end
)
Tokenizer.setParseAction(parseAction)
