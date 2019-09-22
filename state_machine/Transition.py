from uuid import uuid4
from typing import List

from state_machine.Condition import Condition


class Transition:

    def __init__(self, from_state, to_state, conditions: List[Condition]):

        self.from_state = from_state
        self.to_state = to_state
        self.conditions = conditions
        self._id = uuid4()

    def is_allowed(self, data):

        return all([condition.check_condition(data) for condition in self.conditions])

    def __hash__(self):

        return hash(self._id)