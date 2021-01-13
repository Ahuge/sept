class SeptError(RuntimeError):
    def __init__(self, location, message):
        super(SeptError, self).__init__(message)
        self.location = location


class TokenNotFoundError(SeptError):
    pass


class OperatorError(SeptError):
    pass


class ParsingError(SeptError):
    def __init__(self, location, message):
        super(ParsingError, self).__init__(location, message)


class MultipleParsingError(ParsingError):
    def __init__(self, errors):
        location = -1
        if errors:
            location = errors[0].location
        super(MultipleParsingError, self).__init__(
            location=location,
            message="\n".join(str(error) for error in errors)
        )
        self.errors = errors


class InvalidCharacterParsingError(ParsingError):
    MSG_TEMPLATE = 'Error parsing expression: "{expr}". Expected "{expect}", found "{found}" at col:{s_col}-{e_col}'

    def __init__(self, expression, expected_char, actual_char, start_col, end_col):
        self.expression = expression
        self.expected_char = expected_char
        self.actual_char = actual_char
        self.start_col = start_col
        self.end_col = end_col

        msg = self.MSG_TEMPLATE.format(
            expr=self.expression[self.start_col : self.end_col],
            expect=self.expected_char,
            found=self.actual_char,
            s_col=self.start_col,
            e_col=self.end_col,
        )

        super(InvalidCharacterParsingError, self).__init__(
            location=self.start_col,
            message=msg,
        )


class BalancingParenthesisError(ParsingError):
    def __init__(self, missing_token, substr, start_location, end_location):
        message = (
            'Error: Missing closing "{}" characters for Token '
            'Expression "{}" ({}-{})'.format(
                missing_token,
                substr,
                start_location,
                end_location,
            )
        )

        super(BalancingParenthesisError, self).__init__(
            location=start_location,
            message=message
        )


class OpeningBalancingParenthesisError(BalancingParenthesisError):
    pass


class ClosingBalancingParenthesisError(BalancingParenthesisError):
    pass


class MultipleBalancingError(ParsingError):
    def __init__(self, errors):
        location = -1
        if errors:
            location = errors[0].location
        super(MultipleBalancingError, self).__init__(
            location=location,
            message="\n".join(str(error) for error in errors)
        )
        self.errors = errors


class OperatorNotFoundError(OperatorError):
    pass


class TokenNameAlreadyExists(SeptError):
    pass


class OperatorNameAlreadyExists(SeptError):
    pass


class InvalidOperatorArgumentsError(OperatorError):
    pass


class InvalidOperatorInputDataError(OperatorError):
    pass
