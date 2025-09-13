"""
DFA Minimization using Hopcroft's Algorithm
"""

from .dfa import DFA


class DFAMinimizer:
    """
    DFA Minimizer using Hopcroft's algorithm
    """
    
    def __init__(self):
        pass
    
    def minimize(self, dfa):
        """
        Minimize DFA using Hopcroft's algorithm
        
        Args:
            dfa: DFA object to minimize
            
        Returns:
            Minimized DFA object
        """
        # Create a copy to avoid modifying original
        dfa_copy = dfa.copy()
        
        # Remove unreachable states first
        dfa_copy.remove_unreachable_states()
        
        # If only one state, return as is
        if len(dfa_copy.states) <= 1:
            return dfa_copy
        
        # Initialize partitions
        partitions = self._initialize_partitions(dfa_copy)
        
        # Refine partitions until no more refinement possible
        changed = True
        while changed:
            changed = False
            new_partitions = []
            
            for partition in partitions:
                refined = self._refine_partition(partition, partitions, dfa_copy)
                if len(refined) > 1:
                    changed = True
                new_partitions.extend(refined)
            
            partitions = new_partitions
        
        # Build minimized DFA from partitions
        return self._build_minimized_dfa(dfa_copy, partitions)
    
    def _initialize_partitions(self, dfa):
        """Initialize partitions with accepting and non-accepting states"""
        accepting = []
        non_accepting = []
        
        for state in dfa.states:
            if state in dfa.accept_states:
                accepting.append(state)
            else:
                non_accepting.append(state)
        
        partitions = []
        if accepting:
            partitions.append(accepting)
        if non_accepting:
            partitions.append(non_accepting)
        
        return partitions
    
    def _refine_partition(self, partition, all_partitions, dfa):
        """Refine a partition based on transition behavior"""
        if len(partition) <= 1:
            return [partition]
        
        # Group states by their transition behavior
        groups = {}
        
        for state in partition:
            # Create signature for this state's transitions
            signature = []
            for symbol in sorted(dfa.alphabet):
                if (state, symbol) in dfa.transitions:
                    next_state = dfa.transitions[(state, symbol)]
                    # Find which partition the next state belongs to
                    partition_index = self._find_partition_index(next_state, all_partitions)
                    signature.append(partition_index)
                else:
                    signature.append(-1)  # No transition
            
            signature = tuple(signature)
            
            if signature not in groups:
                groups[signature] = []
            groups[signature].append(state)
        
        return list(groups.values())
    
    def _find_partition_index(self, state, partitions):
        """Find which partition a state belongs to"""
        for i, partition in enumerate(partitions):
            if state in partition:
                return i
        return -1
    
    def _build_minimized_dfa(self, original_dfa, partitions):
        """Build minimized DFA from partitions"""
        # Create state mapping
        state_map = {}
        new_states = []
        
        for i, partition in enumerate(partitions):
            new_state = f"q{i}"
            new_states.append(new_state)
            for old_state in partition:
                state_map[old_state] = new_state
        
        # Find new start state
        new_start_state = state_map[original_dfa.start_state]
        
        # Find new accept states
        new_accept_states = set()
        for old_accept_state in original_dfa.accept_states:
            if old_accept_state in state_map:
                new_accept_states.add(state_map[old_accept_state])
        
        # Build new transitions
        new_transitions = {}
        processed_transitions = set()
        
        for (old_state, symbol), old_next_state in original_dfa.transitions.items():
            if old_state in state_map and old_next_state in state_map:
                new_state = state_map[old_state]
                new_next_state = state_map[old_next_state]
                
                # Avoid duplicate transitions
                transition_key = (new_state, symbol)
                if transition_key not in processed_transitions:
                    new_transitions[transition_key] = new_next_state
                    processed_transitions.add(transition_key)
        
        return DFA(
            states=set(new_states),
            alphabet=original_dfa.alphabet,
            transitions=new_transitions,
            start_state=new_start_state,
            accept_states=new_accept_states
        )
    
    def get_equivalent_states(self, dfa):
        """
        Get groups of equivalent states (for analysis purposes)
        
        Args:
            dfa: DFA to analyze
            
        Returns:
            List of lists, where each inner list contains equivalent states
        """
        dfa_copy = dfa.copy()
        dfa_copy.remove_unreachable_states()
        
        partitions = self._initialize_partitions(dfa_copy)
        
        changed = True
        while changed:
            changed = False
            new_partitions = []
            
            for partition in partitions:
                refined = self._refine_partition(partition, partitions, dfa_copy)
                if len(refined) > 1:
                    changed = True
                new_partitions.extend(refined)
            
            partitions = new_partitions
        
        return partitions
