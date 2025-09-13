"""
Utility functions for DFA operations
"""

import json
from .dfa import DFA


def load_dfa_from_json(filepath):
    """
    Load DFA configuration from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary with DFA configuration
    """
    with open(filepath, 'r') as f:
        config = json.load(f)
    
    # Validate required fields
    required_fields = ['states', 'alphabet', 'transitions', 'start_state', 'accept_states']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    # Convert transitions from list format to dictionary if needed
    if isinstance(config['transitions'], list):
        transition_dict = {}
        for transition in config['transitions']:
            if len(transition) != 3:
                raise ValueError("Each transition must have exactly 3 elements: [from_state, symbol, to_state]")
            from_state, symbol, to_state = transition
            transition_dict[(from_state, symbol)] = to_state
        config['transitions'] = transition_dict
    
    return config


def save_dfa_to_json(dfa, filepath):
    """
    Save DFA to JSON file
    
    Args:
        dfa: DFA object
        filepath: Path to save file
    """
    config = dfa.to_dict()
    
    # Convert transitions to list format for JSON serialization
    transition_list = []
    for (from_state, symbol), to_state in config['transitions'].items():
        transition_list.append([from_state, symbol, to_state])
    
    config['transitions'] = transition_list
    
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)


def format_transitions(transitions):
    """
    Format transitions dictionary for display
    
    Args:
        transitions: Dictionary of transitions
        
    Returns:
        List of formatted transition strings
    """
    formatted = []
    for (from_state, symbol), to_state in sorted(transitions.items()):
        formatted.append(f"δ({from_state}, {symbol}) = {to_state}")
    
    return formatted


def create_dfa_from_dict(config):
    """
    Create DFA object from dictionary configuration
    
    Args:
        config: Dictionary with DFA configuration
        
    Returns:
        DFA object
    """
    return DFA(
        states=config['states'],
        alphabet=config['alphabet'],
        transitions=config['transitions'],
        start_state=config['start_state'],
        accept_states=config['accept_states']
    )


def validate_dfa_config(config):
    """
    Validate DFA configuration dictionary
    
    Args:
        config: Dictionary with DFA configuration
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    required_fields = ['states', 'alphabet', 'transitions', 'start_state', 'accept_states']
    
    # Check required fields
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    states = set(config['states'])
    alphabet = set(config['alphabet'])
    start_state = config['start_state']
    accept_states = set(config['accept_states'])
    transitions = config['transitions']
    
    # Check start state
    if start_state not in states:
        raise ValueError(f"Start state '{start_state}' not in states")
    
    # Check accept states
    if not accept_states.issubset(states):
        invalid_states = accept_states - states
        raise ValueError(f"Accept states not in states: {invalid_states}")
    
    # Check transitions
    if isinstance(transitions, dict):
        for (from_state, symbol), to_state in transitions.items():
            if from_state not in states:
                raise ValueError(f"Transition from state '{from_state}' not in states")
            if symbol not in alphabet:
                raise ValueError(f"Transition symbol '{symbol}' not in alphabet")
            if to_state not in states:
                raise ValueError(f"Transition to state '{to_state}' not in states")
    elif isinstance(transitions, list):
        for transition in transitions:
            if len(transition) != 3:
                raise ValueError("Each transition must have exactly 3 elements")
            from_state, symbol, to_state = transition
            if from_state not in states:
                raise ValueError(f"Transition from state '{from_state}' not in states")
            if symbol not in alphabet:
                raise ValueError(f"Transition symbol '{symbol}' not in alphabet")
            if to_state not in states:
                raise ValueError(f"Transition to state '{to_state}' not in states")
    else:
        raise ValueError("Transitions must be dictionary or list")
    
    return True


def transitions_to_table(transitions, states, alphabet):
    """
    Convert transitions to table format
    
    Args:
        transitions: Dictionary of transitions
        states: List of states
        alphabet: List of symbols
        
    Returns:
        2D list representing transition table
    """
    table = []
    
    # Header row
    header = ['State'] + list(alphabet)
    table.append(header)
    
    # Data rows
    for state in sorted(states):
        row = [state]
        for symbol in alphabet:
            if (state, symbol) in transitions:
                row.append(transitions[(state, symbol)])
            else:
                row.append('-')
        table.append(row)
    
    return table


def table_to_transitions(table):
    """
    Convert transition table to transitions dictionary
    
    Args:
        table: 2D list representing transition table
        
    Returns:
        Dictionary of transitions
    """
    if not table or len(table) < 2:
        raise ValueError("Table must have at least header and one data row")
    
    header = table[0]
    alphabet = header[1:]  # Skip 'State' column
    
    transitions = {}
    
    for row in table[1:]:
        state = row[0]
        for i, symbol in enumerate(alphabet):
            next_state = row[i + 1]
            if next_state != '-' and next_state != '':
                transitions[(state, symbol)] = next_state
    
    return transitions
