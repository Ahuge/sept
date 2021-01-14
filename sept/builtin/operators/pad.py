from sept.operator import Operator


class PadOperator(Operator):
    """
    The <code>pad</code> Operator allows you to pad your token with characters.
    <br>This Operator supports the arguments a number of padding and then any single character.
    <br>
    <br>Examples (name = "1"):
    <br>&emsp;<code>{{pad[4,X]:name}} -> "XXX1"</code>
    <br>&emsp;<code>{{pad[1,X]:name}} -> "1"</code>
    <br>&emsp;<code>{{pad[4,0]:name}} -> "0001"</code>
    """

    name = "pad"

    def is_invalid(self, token_value):
        args = self._args
        if not args or len(args) != 2:
            return (
                "Invalid argument values passed to {name}. We expect two "
                "arguments that are text values.".format(name=self.name)
            )
        try:
            int(self._args[0])
        except (TypeError, ValueError):
            # Could not cast to int
            return "The first input value passed should be a number."
        if len(self._args[1]) > 1:
            return "The padding character as the second input value needs to be a single character/"
        return None

    def execute(self, input_data):
        padding_count, padding_char = self._args
        try:
            padding_count = int(padding_count)
        except (TypeError, ValueError):
            return None

        try:
            template_msg = "{{:{char}>{count}}}".format(
                char=padding_char, count=padding_count
            )
            return template_msg.format(input_data)
        except Exception:
            return None
