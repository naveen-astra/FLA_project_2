"""
Unit tests for DFA Minimizer
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the dfa module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dfa.dfa import DFA
from dfa.minimizer import DFAMinimizer


class TestDFAMinimizer(unittest.TestCase):
    """Test cases for DFA Minimizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.minimizer = DFAMinimizer()
        
        # Simple DFA that cannot be minimized further
        self.minimal_dfa = DFA(
            states={'q0', 'q1', 'q2'},
            alphabet={'0', '1'},
            transitions={
                ('q0', '0'): 'q1',
                ('q0', '1'): 'q0',
                ('q1', '0'): 'q1',
                ('q1', '1'): 'q2',
                ('q2', '0'): 'q1',
                ('q2', '1'): 'q0'
            },
            start_state='q0',
            accept_states={'q2'}
        )
        
        # DFA with equivalent states that can be minimized
        self.redundant_dfa = DFA(
            states={'q0', 'q1', 'q2', 'q3', 'q4'},
            alphabet={'0', '1'},
            transitions={
                ('q0', '0'): 'q1',
                ('q0', '1'): 'q0',
                ('q1', '0'): 'q2',
                ('q1', '1'): 'q3',
                ('q2', '0'): 'q2',
                ('q2', '1'): 'q4',
                ('q3', '0'): 'q2',
                ('q3', '1'): 'q3',
                ('q4', '0'): 'q4',
                ('q4', '1'): 'q4'
            },
            start_state='q0',
            accept_states={'q2', 'q4'}
        )
    
    def test_minimize_already_minimal(self):
        """Test minimization of already minimal DFA"""
        minimized = self.minimizer.minimize(self.minimal_dfa)
        
        # Should have same number of states or fewer
        self.assertLessEqual(len(minimized.states), len(self.minimal_dfa.states))
        
        # Should accept same language (test with several strings)
        test_strings = ['', '0', '1', '01', '10', '101', '1001', '0110']
        
        for string in test_strings:
            with self.subTest(string=string):
                original_result = self.minimal_dfa.simulate(string)
                minimized_result = minimized.simulate(string)
                self.assertEqual(
                    original_result['accepted'], 
                    minimized_result['accepted'],
                    f"Language differs for string '{string}'"
                )
    
    def test_minimize_redundant_dfa(self):
        """Test minimization of DFA with redundant states"""
        original_states = len(self.redundant_dfa.states)
        minimized = self.minimizer.minimize(self.redundant_dfa)
        
        # Should have fewer states
        self.assertLess(len(minimized.states), original_states)
        
        # Should still accept same language
        test_strings = ['', '0', '1', '00', '01', '10', '11', '000', '001', '010', '011']
        
        for string in test_strings:
            with self.subTest(string=string):
                original_result = self.redundant_dfa.simulate(string)
                minimized_result = minimized.simulate(string)
                self.assertEqual(
                    original_result['accepted'], 
                    minimized_result['accepted'],
                    f"Language differs for string '{string}'"
                )
    
    def test_minimize_single_state_dfa(self):
        """Test minimization of single state DFA"""
        single_state_dfa = DFA(
            states={'q0'},
            alphabet={'0', '1'},
            transitions={
                ('q0', '0'): 'q0',
                ('q0', '1'): 'q0'
            },
            start_state='q0',
            accept_states={'q0'}
        )
        
        minimized = self.minimizer.minimize(single_state_dfa)
        
        # Should still have one state
        self.assertEqual(len(minimized.states), 1)
        
        # Should accept all strings
        test_strings = ['', '0', '1', '01', '10', '101']
        for string in test_strings:
            result = minimized.simulate(string)
            self.assertTrue(result['accepted'])
    
    def test_minimize_with_unreachable_states(self):
        """Test minimization of DFA with unreachable states"""
        dfa_with_unreachable = DFA(
            states={'q0', 'q1', 'q2', 'q3'},
            alphabet={'0', '1'},
            transitions={
                ('q0', '0'): 'q1',
                ('q0', '1'): 'q0',
                ('q1', '0'): 'q1',
                ('q1', '1'): 'q2',
                ('q2', '0'): 'q1',
                ('q2', '1'): 'q0',
                # q3 is unreachable
                ('q3', '0'): 'q3',
                ('q3', '1'): 'q3'
            },
            start_state='q0',
            accept_states={'q2'}
        )
        
        minimized = self.minimizer.minimize(dfa_with_unreachable)
        
        # Should not include unreachable state
        self.assertNotIn('q3', [str(state) for state in minimized.states])
        self.assertLessEqual(len(minimized.states), 3)
    
    def test_get_equivalent_states(self):
        """Test getting equivalent states"""
        equivalent_groups = self.minimizer.get_equivalent_states(self.redundant_dfa)
        
        # Should return list of groups
        self.assertIsInstance(equivalent_groups, list)
        
        # Each group should be a list of states
        for group in equivalent_groups:
            self.assertIsInstance(group, list)
            self.assertGreater(len(group), 0)
        
        # All original states should be in some group
        all_states_in_groups = set()
        for group in equivalent_groups:
            all_states_in_groups.update(group)
        
        reachable_states = self.redundant_dfa.get_reachable_states()
        self.assertEqual(all_states_in_groups, reachable_states)
    
    def test_partition_initialization(self):
        """Test initial partition creation"""
        partitions = self.minimizer._initialize_partitions(self.redundant_dfa)
        
        # Should have at least one partition
        self.assertGreater(len(partitions), 0)
        
        # Should separate accepting and non-accepting states
        accepting_partition = None
        non_accepting_partition = None
        
        for partition in partitions:
            if any(state in self.redundant_dfa.accept_states for state in partition):
                accepting_partition = partition
            else:
                non_accepting_partition = partition
        
        # Check that accepting states are in accepting partition
        if accepting_partition:
            for state in accepting_partition:
                self.assertIn(state, self.redundant_dfa.accept_states)
        
        # Check that non-accepting states are in non-accepting partition
        if non_accepting_partition:
            for state in non_accepting_partition:
                self.assertNotIn(state, self.redundant_dfa.accept_states)
    
    def test_partition_refinement(self):
        """Test partition refinement"""
        initial_partitions = self.minimizer._initialize_partitions(self.redundant_dfa)
        
        # Test refinement of a partition
        if len(initial_partitions) > 0:
            partition_to_refine = initial_partitions[0]
            if len(partition_to_refine) > 1:
                refined = self.minimizer._refine_partition(
                    partition_to_refine, 
                    initial_partitions, 
                    self.redundant_dfa
                )
                
                # Should return list of partitions
                self.assertIsInstance(refined, list)
                
                # All states should still be present
                all_refined_states = set()
                for group in refined:
                    all_refined_states.update(group)
                
                self.assertEqual(all_refined_states, set(partition_to_refine))
    
    def test_find_partition_index(self):
        """Test finding partition index for a state"""
        partitions = [['q0', 'q1'], ['q2'], ['q3', 'q4']]
        
        self.assertEqual(self.minimizer._find_partition_index('q0', partitions), 0)
        self.assertEqual(self.minimizer._find_partition_index('q1', partitions), 0)
        self.assertEqual(self.minimizer._find_partition_index('q2', partitions), 1)
        self.assertEqual(self.minimizer._find_partition_index('q3', partitions), 2)
        self.assertEqual(self.minimizer._find_partition_index('q4', partitions), 2)
        self.assertEqual(self.minimizer._find_partition_index('q5', partitions), -1)
    
    def test_minimize_preserves_start_state_reachability(self):
        """Test that minimization preserves start state reachability"""
        minimized = self.minimizer.minimize(self.redundant_dfa)
        
        # Start state should still be present
        self.assertIsNotNone(minimized.start_state)
        self.assertIn(minimized.start_state, minimized.states)
    
    def test_minimize_preserves_alphabet(self):
        """Test that minimization preserves alphabet"""
        minimized = self.minimizer.minimize(self.redundant_dfa)
        
        # Alphabet should be preserved
        self.assertEqual(minimized.alphabet, self.redundant_dfa.alphabet)
    
    def test_minimized_dfa_is_valid(self):
        """Test that minimized DFA is valid"""
        minimized = self.minimizer.minimize(self.redundant_dfa)
        
        # Should be able to create DFA without errors (validation in constructor)
        self.assertIsInstance(minimized, DFA)
        
        # Should have valid transitions
        for (state, symbol), next_state in minimized.transitions.items():
            self.assertIn(state, minimized.states)
            self.assertIn(symbol, minimized.alphabet)
            self.assertIn(next_state, minimized.states)


if __name__ == '__main__':
    unittest.main()
