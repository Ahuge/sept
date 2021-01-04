import six

from sept.errors import InvalidOperatorArgumentsError
from sept.operator import Operator


class SubStringOperator(Operator):
    name = "substr"
    START_KEY = "start"
    END_KEY = "end"
    DATA_TYPES = (six.text_type, six.binary_type)
    keywords = {
        START_KEY: 0,
        END_KEY: None,
    }

    def is_invalid(self, token_value):
        args = self._args
        if not args or len(args) > 2:
            return (
                "Invalid argument values passed to {name}. We expect one "
                "or two arguments that are either a number or either "
                '"start" or "end" text values.'.format(name=self.name)
            )
        if isinstance(token_value, self.DATA_TYPES):
            # Is valid
            return None
        elif not token_value:
            # Value is empty
            return "Missing text value"
        return "Value must be one of the following data types ({})".format(
            self.DATA_TYPES
        )

    def execute(self, input_data):
        args = self._args
        if len(args) == 1:
            # Only have a start value
            start = args[0]
            end = None
        elif len(args) == 2:
            start = args[0]
            end = args[1]
        else:
            err = (
                "The `substr` Operator does not support the following "
                "arguments: {}".format(args)
            )
            raise InvalidOperatorArgumentsError(err)

        start = start.lower().strip(" ")
        if end:
            end = end.lower().strip(" ")

        if start in self.keywords:
            start = self.keywords.get(start)
        else:
            start = int(start)
        if end in self.keywords:
            end = self.keywords.get(end)
        elif end is not None:
            end = int(end)

        if end:
            return input_data[start:end]
        else:
            return input_data[start:]
