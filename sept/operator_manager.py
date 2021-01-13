from sept.errors import OperatorNotFoundError, OperatorNameAlreadyExists


class OperatorManager(object):
    def __init__(self):
        super(OperatorManager, self).__init__()
        self._cache = {}

        from sept.builtin.operators import ALL_OPERATORS

        for operator_klass in ALL_OPERATORS:
            self._cache[operator_klass.name] = operator_klass

    @property
    def operators(self):
        # Don't include the NULL operator
        return sorted(
            filter(lambda op: op._private is False, self._cache.values()),
            key=lambda op: op.name,
        )

    def add_custom_operators(self, custom_operators, dont_overwrite=True):
        for custom_operator in custom_operators:
            if custom_operator.name in self._cache and dont_overwrite:
                raise OperatorNameAlreadyExists(
                    "An Operator with the name {name} already exists as "
                    "{value}. If you wish to overwrite that value, make sure "
                    "you pass `dont_overwrite=True` when adding custom "
                    "operators.".format(
                        name=custom_operator.name,
                        value=self._cache[custom_operator.name],
                    )
                )
            self._cache[custom_operator.name] = custom_operator()

    def getOperator(self, operator_name, args=None):
        if operator_name in self._cache:
            operator_klass = self._cache[operator_name]
            return operator_klass.create(args)
        raise OperatorNotFoundError(
            "Could not find an Operator with the name {}".format(operator_name)
        )
