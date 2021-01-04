from .token import Token
from .operator import Operator
from .parser import PathTemplateParser

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
