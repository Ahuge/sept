from sept.operator import Operator


class NullOperator(Operator):
    name = "NULL"

    def is_invalid(self, token_value):
        return None

    def execute(self, input_data):
        return input_data
