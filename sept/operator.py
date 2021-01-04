class Operator(object):
    name = NotImplementedError

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
