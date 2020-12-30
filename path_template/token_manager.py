from path_template.errors import TokenNotFoundError, TokenNameAlreadyExists

from path_template.token import ResolvedToken


class TokenManager(object):
    def __init__(self):
        super(TokenManager, self).__init__()
        self._cache = {}

        from path_template.builtin.tokens import ALL_TOKENS
        for token_klass in ALL_TOKENS:
            self._cache[token_klass.name] = token_klass()

    def add_custom_tokens(self, custom_tokens, dont_overwrite=True):
        for custom_token in custom_tokens:
            if custom_token.name in self._cache and dont_overwrite:
                raise TokenNameAlreadyExists(
                    "A Token with the name {name} already exists as {value}. "
                    "If you wish to overwrite that value, make sure you pass "
                    "`dont_overwrite=True` when adding custom tokens.".format(
                        name=custom_token.name,
                        value=self._cache[custom_token.name],
                    )
                )
            self._cache[custom_token.name] = custom_token()

    def _bind_token(self, token_name, operator_instance, tok_start, tok_end, orig_str):
        if isinstance(token_name, ResolvedToken):
            # It is a nested ResolvedToken.
            resolved_token = token_name
            raw_token = self._cache[resolved_token.raw_token]
            operators = resolved_token.operators
            operators.append(operator_instance)
        else:
            raw_token = self._cache[token_name]
            operators = [operator_instance]

        return ResolvedToken(
            raw_token=raw_token,
            operators=operators,
            tok_start=tok_start,  # We don't care about the child start
            tok_end=tok_end,      # We don't care about the child end
            # This is because we will replace the entire nested token
            original_string=orig_str
        )

    def bind_token(self, token, operator, tok_start, tok_end, tok_original_string):
        if token not in self._cache and not isinstance(token, ResolvedToken):
            error = "Could not find a registered token matching: \"{name}\"\n" \
                    "Found from {start} to {end}: \"{msg}\""
            raise TokenNotFoundError(error.format(
                name=token,
                start=tok_start,
                end=tok_end,
                msg=tok_original_string
            ))
        return self._bind_token(
            token_name=token,
            operator_instance=operator,
            tok_start=tok_start,
            tok_end=tok_end,
            orig_str=tok_original_string
        )
