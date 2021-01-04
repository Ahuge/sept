from .lower import LowerOperator
from .upper import UpperOperator
from .substr import SubStringOperator
from .replace import ReplaceOperator
from .null import NullOperator
ALL_OPERATORS = [
    LowerOperator,
    UpperOperator,
    SubStringOperator,
    NullOperator,
    ReplaceOperator,
]
