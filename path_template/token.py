from path_template.errors import InvalidOperatorInputDataError


class Token(object):
    token_name = NotImplementedError

    def getValue(self, data):
        raise NotImplementedError


class ResolvedToken(object):
    def __init__(self, raw_token, operators, tok_start, tok_end, original_string):
        """

        :param Token raw_token:
        :param list operators:
        :param int tok_start:
        :param int tok_end:
        :param str original_string:
        """
        super(ResolvedToken, self).__init__()
        # Used to pull `getValue` and other data from
        self.raw_token = raw_token
        self.operators = operators
        self.tok_start = tok_start
        self.tok_end = tok_end
        self.original_string = original_string

    def execute(self, version_data):
        source_data = self.raw_token.getValue(version_data)
        transformed_data = source_data

        previous_operator = None
        for operator in self.operators:
            is_invalid_data = operator.invalid(transformed_data)
            if is_invalid_data:
                error = "The Operator {opname} received invalid data and " \
                        "could not continue. {opname} threw the error: " \
                        "\"{errmsg}\". The previous Operator was {prevop}, " \
                        "maybe the error originated there?"
                raise InvalidOperatorInputDataError(error.format(
                    opname=operator.name,
                    errmsg=is_invalid_data,
                    prevop=previous_operator,
                ))
            transformed_data = operator.execute(transformed_data)
            previous_operator = operator
        return transformed_data
