import six

from sept.errors import InvalidOperatorArgumentsError
from sept.operator import Operator


class ReplaceOperator(Operator):
    """
    The <code>replace</code> Operator allows you to find and replace characters in your Token.
    <br>
    <br>Examples (name = "alex"):
    <br>&emsp;<code>{{replace[ex,an]:name}}&nbsp;&nbsp;   -> "alan"</code>
    <br>&emsp;<code>{{replace[kite,dog:name}} -> "alex"</code>
    """

    name = "replace"
    args = [
        {
            "name": "Find String",
            "description": "The characters that you want to search for and replace",
            "required": True,
        },
        {
            "name": "Replace String",
            "description": 'The characters that you want to replace the "Find String" with.',
            "required": True,
        },
    ]
    SPACE = "\\s"
    DATA_TYPES = (six.text_type, six.binary_type)
    keywords = {
        SPACE: " ",
    }

    def is_invalid(self, token_value):
        args = self._args
        if not args or len(args) != 2:
            return (
                "Invalid argument values passed to {name}. We expect two "
                "arguments that are text values.".format(name=self.name)
            )
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
        src_char, dst_char = self._args

        for special_character in self.keywords:
            replacement = self.keywords[special_character]
            try:
                src_char = src_char.replace(special_character, replacement)
                dst_char = dst_char.replace(special_character, replacement)
            except Exception as err:
                print(str(err))

        try:
            output_data = input_data.replace(src_char, dst_char)
        except Exception as err:
            raise InvalidOperatorArgumentsError(
                "Error replacing {src} with {dst}. Error: {err}".format(
                    src=src_char, dst=dst_char, err=str(err)
                )
            )
        return output_data
