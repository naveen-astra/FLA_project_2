"""
DFA (Deterministic Finite Automaton) class implementation
"""

class DFA:
    """
    Deterministic Finite Automaton implementation
    """
    
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        Initialize DFA
        
        Args:
            states: Set of states
            alphabet: Set of input symbols
            transitions: Dictionary of transitions {(state, symbol): next_state}
            start_state: Initial state
            accept_states: Set of accepting states
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)
        
        # Validate DFA
        self._validate()
    
    def _validate(self):
        """Validate DFA properties"""
        # Check if start state is in states
        if self.start_state not in self.states:
            raise ValueError(f"Start state {self.start_state} not in states")
        
        # Check if accept states are subset of states
        if not self.accept_states.issubset(self.states):
            raise ValueError("Accept states must be subset of states")
        
        # Check transitions
        for (state, symbol), next_state in self.transitions.items():
            if state not in self.states:
                raise ValueError(f"State {state} in transition not in states")
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol {symbol} in transition not in alphabet")
            if next_state not in self.states:
                raise ValueError(f"Next state {next_state} in transition not in states")
    
    def simulate(self, input_string):
        """
        Simulate DFA on input string
        
        Args:
            input_string: String to process
            
        Returns:
            Dictionary with simulation results
        """
        current_state = self.start_state
        path = [current_state]
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return {
                    'accepted': False,
                    'path': path,
                    'final_state': current_state,
                    'error': f"Symbol '{symbol}' not in alphabet"
                }
            
            # Check if transition exists
            if (current_state, symbol) not in self.transitions:
                return {
                    'accepted': False,
                    'path': path,
                    'final_state': current_state,
                    'error': f"No transition from state '{current_state}' on symbol '{symbol}'"
                }
            
            current_state = self.transitions[(current_state, symbol)]
            path.append(current_state)
        
        # Check if final state is accepting
        accepted = current_state in self.accept_states
        
        return {
            'accepted': accepted,
            'path': path,
            'final_state': current_state
        }
    
    def is_complete(self):
        """Check if DFA is complete (has transition for every state-symbol pair)"""
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
        return True
    
    def get_reachable_states(self):
        """Get all states reachable from start state"""
        reachable = set()
        stack = [self.start_state]
        
        while stack:
            state = stack.pop()
            if state in reachable:
                continue
            
            reachable.add(state)
            
            # Add all states reachable from current state
            for symbol in self.alphabet:
                if (state, symbol) in self.transitions:
                    next_state = self.transitions[(state, symbol)]
                    if next_state not in reachable:
                        stack.append(next_state)
        
        return reachable
    
    def remove_unreachable_states(self):
        """Remove unreachable states from DFA"""
        reachable = self.get_reachable_states()
        
        # Update states
        self.states = reachable
        
        # Update accept states
        self.accept_states = self.accept_states.intersection(reachable)
        
        # Update transitions
        new_transitions = {}
        for (state, symbol), next_state in self.transitions.items():
            if state in reachable and next_state in reachable:
                new_transitions[(state, symbol)] = next_state
        
        self.transitions = new_transitions
    
    def copy(self):
        """Create a copy of the DFA"""
        return DFA(
            states=self.states.copy(),
            alphabet=self.alphabet.copy(),
            transitions=self.transitions.copy(),
            start_state=self.start_state,
            accept_states=self.accept_states.copy()
        )
    
    def to_dict(self):
        """Convert DFA to dictionary representation"""
        return {
            'states': list(self.states),
            'alphabet': list(self.alphabet),
            'transitions': self.transitions,
            'start_state': self.start_state,
            'accept_states': list(self.accept_states)
        }
    
    def __str__(self):
        """String representation of DFA"""
        return f"DFA(states={len(self.states)}, alphabet={self.alphabet}, start={self.start_state}, accept={self.accept_states})"
