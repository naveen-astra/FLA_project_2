"""
Unit tests for DFA class
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the dfa module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dfa.dfa import DFA


class TestDFA(unittest.TestCase):
    """Test cases for DFA class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Simple DFA that accepts strings ending in '01'
        self.simple_dfa = DFA(
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
    
    def test_dfa_initialization(self):
        """Test DFA initialization"""
        self.assertEqual(self.simple_dfa.states, {'q0', 'q1', 'q2'})
        self.assertEqual(self.simple_dfa.alphabet, {'0', '1'})
        self.assertEqual(self.simple_dfa.start_state, 'q0')
        self.assertEqual(self.simple_dfa.accept_states, {'q2'})
    
    def test_invalid_start_state(self):
        """Test DFA with invalid start state"""
        with self.assertRaises(ValueError):
            DFA(
                states={'q0', 'q1'},
                alphabet={'0', '1'},
                transitions={},
                start_state='q3',  # Not in states
                accept_states=set()
            )
    
    def test_invalid_accept_states(self):
        """Test DFA with invalid accept states"""
        with self.assertRaises(ValueError):
            DFA(
                states={'q0', 'q1'},
                alphabet={'0', '1'},
                transitions={},
                start_state='q0',
                accept_states={'q3'}  # Not in states
            )
    
    def test_invalid_transitions(self):
        """Test DFA with invalid transitions"""
        with self.assertRaises(ValueError):
            DFA(
                states={'q0', 'q1'},
                alphabet={'0', '1'},
                transitions={('q0', '2'): 'q1'},  # '2' not in alphabet
                start_state='q0',
                accept_states=set()
            )
    
    def test_simulate_accepted_strings(self):
        """Test simulation of accepted strings"""
        test_cases = ['01', '101', '1001', '0101']
        
        for string in test_cases:
            with self.subTest(string=string):
                result = self.simple_dfa.simulate(string)
                self.assertTrue(result['accepted'], f"String '{string}' should be accepted")
                self.assertEqual(result['final_state'], 'q2')
    
    def test_simulate_rejected_strings(self):
        """Test simulation of rejected strings"""
        test_cases = ['', '1', '10', '00', '11', '010']
        
        for string in test_cases:
            with self.subTest(string=string):
                result = self.simple_dfa.simulate(string)
                self.assertFalse(result['accepted'], f"String '{string}' should be rejected")
    
    def test_simulate_invalid_symbol(self):
        """Test simulation with invalid symbols"""
        result = self.simple_dfa.simulate('01a')
        self.assertFalse(result['accepted'])
        self.assertIn('error', result)
        self.assertIn('not in alphabet', result['error'])
    
    def test_simulate_missing_transition(self):
        """Test simulation with missing transition"""
        # Create DFA with missing transition
        incomplete_dfa = DFA(
            states={'q0', 'q1'},
            alphabet={'0', '1'},
            transitions={('q0', '0'): 'q1'},  # Missing ('q0', '1') transition
            start_state='q0',
            accept_states={'q1'}
        )
        
        result = incomplete_dfa.simulate('01')
        self.assertFalse(result['accepted'])
        self.assertIn('error', result)
        self.assertIn('No transition', result['error'])
    
    def test_is_complete(self):
        """Test DFA completeness check"""
        # Simple DFA is complete
        self.assertTrue(self.simple_dfa.is_complete())
        
        # Create incomplete DFA
        incomplete_dfa = DFA(
            states={'q0', 'q1'},
            alphabet={'0', '1'},
            transitions={('q0', '0'): 'q1'},  # Missing transitions
            start_state='q0',
            accept_states={'q1'}
        )
        self.assertFalse(incomplete_dfa.is_complete())
    
    def test_get_reachable_states(self):
        """Test getting reachable states"""
        reachable = self.simple_dfa.get_reachable_states()
        self.assertEqual(reachable, {'q0', 'q1', 'q2'})
        
        # DFA with unreachable state
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
        
        reachable = dfa_with_unreachable.get_reachable_states()
        self.assertEqual(reachable, {'q0', 'q1', 'q2'})
    
    def test_remove_unreachable_states(self):
        """Test removing unreachable states"""
        # DFA with unreachable state
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
            accept_states={'q2', 'q3'}
        )
        
        original_states = len(dfa_with_unreachable.states)
        dfa_with_unreachable.remove_unreachable_states()
        
        self.assertEqual(dfa_with_unreachable.states, {'q0', 'q1', 'q2'})
        self.assertEqual(dfa_with_unreachable.accept_states, {'q2'})
        self.assertLess(len(dfa_with_unreachable.states), original_states)
    
    def test_copy(self):
        """Test DFA copying"""
        dfa_copy = self.simple_dfa.copy()
        
        # Check that copy has same properties
        self.assertEqual(dfa_copy.states, self.simple_dfa.states)
        self.assertEqual(dfa_copy.alphabet, self.simple_dfa.alphabet)
        self.assertEqual(dfa_copy.transitions, self.simple_dfa.transitions)
        self.assertEqual(dfa_copy.start_state, self.simple_dfa.start_state)
        self.assertEqual(dfa_copy.accept_states, self.simple_dfa.accept_states)
        
        # Check that they are independent objects
        dfa_copy.states.add('q3')
        self.assertNotEqual(dfa_copy.states, self.simple_dfa.states)
    
    def test_to_dict(self):
        """Test DFA to dictionary conversion"""
        dfa_dict = self.simple_dfa.to_dict()
        
        expected_keys = ['states', 'alphabet', 'transitions', 'start_state', 'accept_states']
        for key in expected_keys:
            self.assertIn(key, dfa_dict)
        
        self.assertEqual(set(dfa_dict['states']), self.simple_dfa.states)
        self.assertEqual(set(dfa_dict['alphabet']), self.simple_dfa.alphabet)
        self.assertEqual(dfa_dict['start_state'], self.simple_dfa.start_state)
        self.assertEqual(set(dfa_dict['accept_states']), self.simple_dfa.accept_states)


if __name__ == '__main__':
    unittest.main()
