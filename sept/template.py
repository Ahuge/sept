from sept.template_tokenizer import Tokenizer
from sept.balancer import ParenthesisBalancer
from sept.errors import (
    SeptError,
    ParsingError,
    MultipleBalancingError,
    OperatorNotFoundError,
    TokenNotFoundError,
    InvalidOperatorInputDataError,
)


class _RawTokenExpression(object):
    def __init__(self, text, offset):
        super(_RawTokenExpression, self).__init__()
        self.text = text
        self.offset = offset

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text


class Template(object):
    def __init__(self):
        super(Template, self).__init__()
        self._template_str = ""
        self._resolved_tokens = []

    @classmethod
    def _gather_match(cls, match, tmanager, omanager, offset=0, default_fallback=False):
        _Operator = omanager.getOperator("NULL")

        if match.Operator:
            args = None
            if match.Args:
                args = match.Args
            try:
                _Operator = omanager.getOperator(match.Operator, args=args)
            except OperatorNotFoundError as err:
                raise ParsingError(
                    location=match.start + offset,
                    length=match.end - match.start,
                    message=str(err),
                )
        if match.child:
            resolved_token = cls._gather_match(
                match=match.child,
                tmanager=tmanager,
                omanager=omanager,
                default_fallback=default_fallback,
            )
            try:
                resolved_token = tmanager.bind_token(
                    token=resolved_token,
                    operator=_Operator,
                    tok_start=match.start + offset,
                    tok_end=match.end + offset,
                    tok_original_string=match.original_str,
                    default_fallback=default_fallback,
                )
            except TokenNotFoundError as err:
                raise ParsingError(
                    location=match.start + offset,
                    length=match.end - match.start,
                    message=str(err),
                )
        elif match.Token:
            try:
                resolved_token = tmanager.bind_token(
                    token=match.Token,
                    operator=_Operator,
                    tok_start=match.start + offset,
                    tok_end=match.end + offset,
                    tok_original_string=match.original_str,
                    default_fallback=default_fallback,
                )
            except TokenNotFoundError as err:
                raise ParsingError(
                    location=match.start + offset,
                    length=match.end - match.start,
                    message=str(err),
                )
        else:
            # raise ParsingError("Found Operator without corresponding token.")
            # TODO: Add location in error
            raise RuntimeError("Found Operator without corresponding token.")
        return resolved_token

    @classmethod
    def _balance_template_str(cls, template_str):
        expression_locations, errors = ParenthesisBalancer.parse_string(template_str)
        expressions = []
        for start_index, end_index in expression_locations:
            try:
                _expr = _RawTokenExpression(
                    text=template_str[start_index : end_index + 1], offset=start_index
                )
                expressions.append(_expr)
            except IndexError:
                # Unclear how we got here, probably a bug in balancer
                raise SeptError("Error extracting Token Expressions")
        if errors:
            raise MultipleBalancingError(errors)
        return expressions

    @classmethod
    def sanitize_template_str(cls, template_str):
        return template_str.replace(" ", "")

    @classmethod
    def from_template_str(
        cls, template_str, tmanager, omanager, default_fallback=False
    ):
        matches = []

        template_expressions = cls._balance_template_str(template_str)
        sanitized_template_str = ""
        sanitized_offset = 0

        last_template_expr_end = 0
        for template_expression in template_expressions:
            sanitized_template_str += template_str[
                last_template_expr_end : template_expression.offset
            ]
            last_template_expr_end = template_expression.offset + len(
                template_expression.text
            )

            sanitized_expr = cls.sanitize_template_str(str(template_expression))
            sanitized_template_str += sanitized_expr
            for results, tok_start, tok_end in Tokenizer.scanString(sanitized_expr):
                match = results.match
                resolved_token = cls._gather_match(
                    match=match,
                    tmanager=tmanager,
                    omanager=omanager,
                    offset=template_expression.offset + sanitized_offset,
                    default_fallback=default_fallback,
                )
                matches.append(resolved_token)
            sanitized_offset += len(sanitized_expr) - len(template_expression)

        sanitized_template_str += template_str[last_template_expr_end:]
        T = Template()
        T._template_str = sanitized_template_str
        T._resolved_tokens = matches
        return T

    def resolve(self, data):
        offset = 0
        result_str = self._template_str
        for resolved_token in self._resolved_tokens:
            start = resolved_token.start
            end = resolved_token.end
            before, target, after = (
                result_str[: start + offset],
                result_str[start + offset : end + offset],
                result_str[end + offset :],
            )
            try:
                transformed = resolved_token.execute(data)
            except InvalidOperatorInputDataError as err:
                raise ParsingError(location=start, length=end - start, message=str(err))
            result_str = before + transformed + after
            offset += len(transformed) - len(target)

        return result_str
