from sept.token import Token


def DefaultTokenFactory(token_name):
    class DefaultFallbackToken(Token):
        name = token_name

        def getValue(self, data):
            return data.get(token_name)

    return DefaultFallbackToken
