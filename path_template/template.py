from path_template.template_tokenizer import Tokenizer


class Template(object):
    def __init__(self):
        super(Template, self).__init__()
        self._template_str = ""
        self._resolved_tokens = []

    @classmethod
    def _gather_match(cls, match, tmanager, omanager):
        _Operator = omanager.getOperator("NULL")

        if match.Operator:
            args = None
            if match.Args:
                args = match.Args
            _Operator = omanager.getOperator(match.Operator, args=args)
        if match.child:
            resolved_token = cls._gather_match(match.child, tmanager, omanager)
            resolved_token = tmanager.bind_token(
                token=resolved_token, operator=_Operator,
                tok_start=match.start, tok_end=match.end,
                tok_original_string=match.original_str,
            )
        elif match.Token:
            resolved_token = tmanager.bind_token(
                token=match.Token, operator=_Operator,
                tok_start=match.start, tok_end=match.end,
                tok_original_string=match.original_str,
            )
        else:
            # raise ParsingError("Found Operator without corresponding token.")
            # TODO: Add location in error
            raise RuntimeError("Found Operator without corresponding token.")
        return resolved_token

    @classmethod
    def from_template_str(cls, template_str, tmanager, omanager):
        matches = []

        for match, tok_start, tok_end in Tokenizer.scanString(template_str):
            resolved_token = cls._gather_match(match, tmanager, omanager)
            matches.append(resolved_token)
        T = Template()
        T._template_str = template_str
        T._resolved_tokens = matches
        return T

    def resolve(self, data):
        offset = 0
        result_str = self._template_str
        for resolved_token in self._resolved_tokens:
            start = resolved_token.start
            end = resolved_token.end
            before, target, after = (
                result_str[:start+offset],
                result_str[start+offset:end+offset],
                result_str[end+offset:]
            )
            transformed = resolved_token.execute(data)
            result_str = before + transformed + after
            offset += len(transformed) - len(target)

        return result_str
