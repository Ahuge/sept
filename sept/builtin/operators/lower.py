from sept.operator import Operator


class LowerOperator(Operator):
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
