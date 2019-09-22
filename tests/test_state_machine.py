from unittest import TestCase

from state_machine.StateMachine import StateMachine, DFA, DuplicateStateError
from state_machine.State import State
from state_machine.Transition import Transition
from state_machine.Condition import Condition


class StateMachineTestCase(TestCase):

    def test_add_states(self):

        states = [State(i) for i in range(3)]
        sm = StateMachine(states)

        self.assertEqual(len(sm._states), 3)
        for state in states:
            self.assertIn(state, sm)
            self.assertEqual(sm._states[state], set())

    def test_add_duplicate_states(self):

        states = [State(1), State(2)]
        sm = StateMachine()
        sm.add_state(states[0])
        sm.add_state(states[1])
        with self.assertRaises(DuplicateStateError):
            sm.add_state(states[0])

    def test_initial_state(self):

        states = [State(i) for i in range(3)]
        sm = StateMachine(states, initial_state=states[1])

        self.assertEqual(sm.current_state, states[1])

    def test_add_explicit_states_and_transition(self):

        states = [State(1), State(2)]
        sm = StateMachine(states)
        c = Condition('.', 5, '=')
        sm.add_transition(states[0], states[1], [c])

        self.assertEqual(len(sm), 2)
        self.assertEqual(len(sm._states[states[0]]), 1)

    def test_add_implicit_states_and_transition(self):

        sm = StateMachine()
        c = Condition('.', 5, '=')
        state1 = State(1)
        state2 = State(2)
        sm.add_transition(state1, state2, [c])

        self.assertEqual(len(sm), 2)
        self.assertEqual(len(sm._states[state1]), 1)

    def test_dfa_allowed_transition(self):

        states = [State(1), State(2)]
        sm = DFA(states, initial_state=states[0])
        c1 = Condition('.', 5, '=')
        c2 = Condition('.', 7, '>')
        sm.add_transition(states[0], states[1], [c1])
        sm.add_transition(states[0], states[1], [c2])

        sm.advance(5)
        self.assertEqual(sm.current_state, states[1])

        sm.current_state = states[0]
        sm.advance(10)
        self.assertEqual(sm.current_state, states[1])

        sm.current_state = states[0]
        sm.advance(6)
        self.assertEqual(sm.current_state, states[0])
