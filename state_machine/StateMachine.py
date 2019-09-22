from abc import abstractmethod
from typing import List

from state_machine.State import State
from state_machine.Transition import Transition
from state_machine.Condition import Condition


class DuplicateStateError(Exception):
    """ Raised if an attempt is made to add an existing state """


class UninitializedStateMachineError(Exception):
    """ Raised when an attempt is made to advance the state machine without initializing it """


class StateMachine:

    def __init__(self, states=None, initial_state=None):

        self._states = {}
        if states:
            for state in states:
                self._states.setdefault(state, set())

        self.current_state = initial_state

    def add_state(self, state):

        if state in self._states:
            raise DuplicateStateError(f'State {state} is already part of the state machine.')

        self._states.setdefault(state, set())

    def add_transition(self, from_state, to_state, conditions: List[Condition]):
        """
        Adds a conditional transition between two states.
        :param from_state: The state to transition from.
        :param to_state: The state to transition to.
        :param conditions: The conditions to be satisfied before the transition can occur
        :return:
        """

        if from_state not in self:
            self.add_state(from_state)
        if to_state not in self:
            self.add_state(to_state)

        self._states[from_state].add(Transition(from_state, to_state, conditions))

    def __contains__(self, item):

        return item in self._states

    def __len__(self):

        return len(self._states.keys())

    @abstractmethod
    def advance(self, data):
        raise NotImplemented


class DFAMultipleTransitionsError(Exception):
    """ Raised when a DFA has multiple allowed transitions for a given input """


class DFA(StateMachine):

    def advance(self, inp):

        if not self.current_state:
            raise UninitializedStateMachineError('State machine must have its initial state set.')

        potential_transitions = self._states[self.current_state]
        allowed_transitions = set()
        for transition in potential_transitions:
            if transition.is_allowed(inp):
                allowed_transitions.add(transition)
        if len(allowed_transitions) > 1:
            raise DFAMultipleTransitionsError('Multiple transitions found in a DFA.')
        elif len(allowed_transitions) == 0:
            # put in some conditional logic here about what to do depending on flag
            # for now just do nothing
            pass
        else:
            transition = list(allowed_transitions)[0]
            self.current_state = transition.to_state
