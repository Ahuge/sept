import six

from sept.errors import InvalidOperatorArgumentsError
from sept.operator import Operator


class SubStringOperator(Operator):
    """
    The <code>substr</code> Operator allows you to return a subset of the Token.
    <br>This Operator supports the arguments "start" and "end" as well as numerical indexes from zero.
    <br>
    <br>Examples (name = "alex"):
    <br>&emsp;<code>{{substr[start,2]:name}} -> "al"</code>
    <br>&emsp;<code>{{substr[0,2]:name}} &nbsp; &nbsp;&nbsp;&nbsp;-> "al"</code>
    <br>&emsp;<code>{{substr[0,end]:name}} &nbsp;&nbsp;-> "alex"</code>
    <br>&emsp;<code>{{substr[1,3]:name}} &nbsp; &nbsp;&nbsp;&nbsp;-> "le"</code>
    """

    name = "substr"
    args = [
        {
            "name": "Start Location",
            "description": 'The location we want to start our subset from. This supports numbers as well as "end" and "start"',
            "required": True,
        },
        {
            "name": "End Location",
            "description": 'The location we want to end our subset at. This supports numbers as well as "end" and "start"',
            "required": False,
        },
    ]
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
        if len(args) == 1:
            start = args
            end = self.END_KEY
        else:
            start, end = args

        if start not in self.keywords:
            try:
                int(start)
            except ValueError:
                return (
                    "Invalid input value passed to {name}. "
                    "We expect the first argument to be a number or either "
                    '"start" or "end" values. '
                    "{value} was passed instead.".format(name=self.name, value=start)
                )

        if end not in self.keywords:
            try:
                int(end)
            except ValueError:
                return (
                    "Invalid input value passed to {name}. "
                    "We expect the second argument to be a number or either "
                    '"start" or "end" values. '
                    "{value} was passed instead.".format(name=self.name, value=end)
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
