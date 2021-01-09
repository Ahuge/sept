import os
import webbrowser

import six

from sept import PathTemplateParser, Token, Operator


# Custom Tokens
class FirstNameToken(Token):
    """
    The <code>firstname</code> Token will return the "first_name" value from the user data dictionary.
    """
    name = "firstname"

    def getValue(self, data):
        return data.get("user", {}).get("first_name")


class LastNameToken(Token):
    """
    The <code>lastname</code> Token will return the "last_name" value from the user data dictionary.
    """
    name = "lastname"

    def getValue(self, data):
        return data.get("user", {}).get("last_name")


# Custom Operator
class FirstCharacterOperator(Operator):
    """
    The <code>firstletter</code> Operator allows you to return the first letter of the Token.
    <br>
    <br>Examples (name = "alex"):
    <br>&emsp;<code>{{firstletter:name}}&nbsp;&nbsp;   -> "a"</code>
    """
    name = "firstletter"
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

    def execute(self, token_value, *args, **kwargs):
        return token_value[0]


def get_additional_tokens():
    custom_tokens = [
        FirstNameToken,
        LastNameToken,
    ]
    return custom_tokens


def get_additional_operators():
    return [
        FirstCharacterOperator,
    ]


custom_template = "/home/{{firstletter: firstname}}{{lastname}}"
additional_tokens = get_additional_tokens()
additional_operators = get_additional_operators()
state_data = {
    "user": {
        "first_name": "alex",
        "last_name": "hughes",
        "created_date": "2020-12-29",
    },
}

parser = PathTemplateParser(
    additional_tokens=additional_tokens,
    additional_operators=additional_operators,
)

template_obj = parser.validate_template(custom_template)
resolved_path = template_obj.resolve(state_data)

print(resolved_path)
# /home/ahughes


# Generate and launch documentation
operator_docs = parser.operator_documentation()
token_docs = parser.token_documentation()

operator_docs += "<br><br><hr><br><br>" + token_docs
documentation_path = os.path.join(os.path.dirname(__file__), "documentation.html")
with open(documentation_path, "w") as fh:
    fh.write(operator_docs)

webbrowser.open(documentation_path)