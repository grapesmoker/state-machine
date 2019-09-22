from unittest import TestCase

from state_machine.State import State
from state_machine.Condition import Condition
from state_machine.Transition import Transition


class TransitionsTestCase(TestCase):

    def test_is_transition_allowed(self):

        transition = Transition(State(1), State(2), [Condition('.', 1, '>'), Condition('.', 7, '<')])
        self.assertTrue(transition.is_allowed(5))
        self.assertFalse(transition.is_allowed(10))
        self.assertFalse(transition.is_allowed(0))