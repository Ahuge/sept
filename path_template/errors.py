class PathTemplateError(RuntimeError): pass


class TokenNotFoundError(PathTemplateError): pass
class OperatorNotFoundError(PathTemplateError): pass


class TokenNameAlreadyExists(PathTemplateError): pass
class OperatorNameAlreadyExists(PathTemplateError): pass

class InvalidOperatorArgumentsError(PathTemplateError): pass