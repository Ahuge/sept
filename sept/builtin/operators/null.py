from sept.operator import Operator


class NullOperator(Operator):
    """
    The <code>null</code> Operator will do nothing to you Token.
    <br>
    <br>Examples:
    <br>&emsp;<code>"Alex"  &nbsp; &nbsp;-> "Alex"</code>
    <br>&emsp;<code>"alex"  &nbsp; &nbsp;-> "alex"</code>
    <br>&emsp;<code>"ALEX11" -> "ALEX11"</code>
    """

    name = "NULL"
    _private = True

    def is_invalid(self, token_value):
        return None

    def execute(self, input_data):
        return input_data
