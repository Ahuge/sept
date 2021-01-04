import six

from sept import PathTemplateParser, Token, Operator


# Custom Tokens
class FirstNameToken(Token):
    token_name = "firstname"

    def getValue(self, data):
        return data.get("user", {}).get("first_name")


class LastNameToken(Token):
    token_name = "lastname"

    def getValue(self, data):
        return data.get("user", {}).get("last_name")


# Custom Operator
class FirstCharacterOperator(Operator):
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
        FirstNameToken(),
        LastNameToken(),
    ]
    return custom_tokens


def get_additional_operators():
    return [
        FirstCharacterOperator(),
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

resolved_template = parser.parse(
    template=custom_template,
    data=state_data,
)

print(resolved_template)
# /home/ahughes


template_str = "{{upper:{{lower:sequence}}}}/{{subStr[0,3]:shot}}"
