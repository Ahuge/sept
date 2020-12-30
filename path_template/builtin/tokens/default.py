from path_template.token import Token


def DefaultTokenFactory(token_name):
    class DefaultFallbackToken(Token):
        token_name = None

        def getValue(self, data):
            return data.get(token_name)

    return DefaultFallbackToken
