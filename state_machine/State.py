class State:
    """
    States are just wrappers around a label and possibly some additional data.
    """
    def __init__(self, label, data=None):
        """
        Initialize a state.
        :param label: Any hashable.
        :param data: Any additional data that the state should store.
        """
        self.label = label
        self._data = data

    def __hash__(self):

        return hash(self.label)

    def __eq__(self, other):

        return hash(self) == hash(other)