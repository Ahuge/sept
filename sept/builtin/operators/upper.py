from sept.operator import Operator


class UpperOperator(Operator):
    """
    The <code>upper</code> Operator will convert your Token to uppercase.
    <br>
    <br>Examples:
    <br>&emsp;<code>"Alex" &nbsp;&nbsp;-> "ALEX"</code>
    <br>&emsp;<code>"alex" &nbsp;&nbsp;-> "ALEX"</code>
    <br>&emsp;<code>"alex11" -> "ALEX11"</code>
    """

    name = "upper"

    def is_invalid(self, token_value):
        if hasattr(token_value, "upper"):
            return None
        return (
            'Value must have an attribute called "upper", usually this '
            "means we expect text data."
        )

    def execute(self, input_data):
        return input_data.upper()
