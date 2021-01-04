from sept.operator import Operator


class UpperOperator(Operator):
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
