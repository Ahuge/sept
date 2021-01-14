class Operator(object):
    """
    The docstring of your Operator is used as the documentation for your
        Operator.
    You should include any freeform text that you would like as well as some
        examples of how your Operator works.
    This docstring should be treated as html code.

    If you wanted to bold your text, you could just do <b>this!</b>
    """

    name = NotImplementedError
    args = [
        # The args class object is used as an argspec for your Operator
        #   `args` should be a list of dict[name, description, required].
        # eg:
        #   args = [
        #       {"name": "myarg1", "description": "This arg gets used for something", "required": True},
        #       {"name": "myarg2", "description": "This is an extra arg, it's optional", "required": False},
        #   ]
    ]

    # Internal...Ignore this
    _private = False

    def __init__(self, args=None):
        super(Operator, self).__init__()
        self._args = args

    @classmethod
    def create(cls, args=None):
        return cls(args=args)

    def execute(self, input_data):
        """
        execute does the actual work of your custom Operator.
        It will take in the data passed and return the transformed data as
            output.

        :param Any input_data:
        :return: The transformed data according to whatever the Operator is
            supposed to do.
        :rtype: Any
        """
        raise NotImplementedError

    def is_invalid(self, token_value):
        """
        is_invalid will check the value the is about to be operated on.
        If the value will not work for some reason (wrong datatype, etc),
            this method should return an error message as a string.

        If it looks good to go, just return None

        :param Any token_value: Data that would be operated on
        :return: A Falsey value if everything is ok, or an error string if not.
        :rtype: None|str
        """
