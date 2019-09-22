

class Condition:

    COMPARATOR_FUNCS = {
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
        "=": lambda x, y: x == y,
        "!=": lambda x, y: not x == y
    }

    def __init__(self, data_spec: str, value, comparator):
        """
        Initialize a condition that will be checked for allowed transitions
        :param data_spec: a string indicating the path to follow through the data
            possible values:
                - "." - check the data object directly
                - "0" - check the 0th element of the data
                - "foo" - check the attr foo of the data
                - "foo.bar" - check attr bar of attr foo of the data
                - "foo.0" - check the 0th element of attr foo of the data
                - etc.
        :param value: the value to which the data should be compared
        :param comparator: the comparison operation to compare the value to the data
            possible values: ">=", "<=", ">", "<", "=", a function
        """
        self.data_spec = [elem for elem in data_spec.split('.') if elem != '']
        self.value = value
        self.comparator = self.COMPARATOR_FUNCS.get(comparator, None)
        if not self.comparator:
            self.comparator = comparator

    def check_condition(self, data):
        """
        Check if the condition is satisfied by the data, subject to the element
        obtained by following the data spec
        :param data: Any object
        """
        data_element = self._extract_data(data, self.data_spec)
        return self.comparator(data_element, self.value)

    @classmethod
    def _extract_data(cls, data, spec):
        """
        Recursively follow the specified path until the desired object is obtained
        :param data:
        :param spec:
        :return:
        """
        if not spec:
            return data

        for i, item in enumerate(spec):
            if item.isdigit():
                idx = int(item)
                return cls._extract_data(data[idx], spec[i+1:])
            else:
                if isinstance(data, dict):
                    return cls._extract_data(data[item], spec[i+1:])
                else:
                    return cls._extract_data(getattr(data, item), spec[i+1:])

