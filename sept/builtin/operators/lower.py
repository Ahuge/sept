from sept.operator import Operator


class LowerOperator(Operator):
    """
    The <code>lower</code> Operator will convert your Token to lowercase.
    <br>
    <br>Examples:
    <br>&emsp;<code>"Alex" &nbsp;&nbsp;-> "alex"</code>
    <br>&emsp;<code>"alex" &nbsp;&nbsp;-> "alex"</code>
    <br>&emsp;<code>"ALEX11" -> "alex11"</code>
    """

    name = "lower"

    def is_invalid(self, token_value):
        if hasattr(token_value, "lower"):
            return None
        return (
            'Value must have an attribute called "lower", usually this '
            "means we expect text data."
        )

    def execute(self, input_data):
        return input_data.lower()
