"""
DFA Minimizer Web Application
Main entry point using Flask framework
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import os
import logging
from config import config
from dfa.dfa import DFA
from dfa.minimizer import DFAMinimizer
from dfa.utils import load_dfa_from_json, format_transitions

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup logging
    if app.config.get('LOG_TO_FILE'):
        log_dir = os.path.dirname(app.config['LOG_FILE'])
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(app.config['LOG_FILE'])
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
    
    return app

# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/simulate')
def simulate():
    """DFA simulation page"""
    return render_template('simulate.html')

@app.route('/minimize')
def minimize():
    """DFA minimization page"""
    return render_template('minimize.html')

@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """API endpoint for DFA simulation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        dfa_config = data.get('dfa')
        input_string = data.get('input_string', '')
        
        if not dfa_config:
            return jsonify({'success': False, 'error': 'DFA configuration is required'}), 400
        
        # Validate input string length
        max_length = app.config.get('MAX_INPUT_STRING_LENGTH', 1000)
        if len(input_string) > max_length:
            return jsonify({
                'success': False, 
                'error': f'Input string too long (max {max_length} characters)'
            }), 400
        
        # Validate DFA configuration
        required_fields = ['states', 'alphabet', 'transitions', 'start_state', 'accept_states']
        for field in required_fields:
            if field not in dfa_config:
                return jsonify({
                    'success': False, 
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate state and alphabet limits
        max_states = app.config.get('MAX_STATES', 100)
        max_alphabet = app.config.get('MAX_ALPHABET_SIZE', 20)
        
        if len(dfa_config['states']) > max_states:
            return jsonify({
                'success': False, 
                'error': f'Too many states (max {max_states})'
            }), 400
        
        if len(dfa_config['alphabet']) > max_alphabet:
            return jsonify({
                'success': False, 
                'error': f'Alphabet too large (max {max_alphabet} symbols)'
            }), 400
        
        # Process transitions - handle both list and dict formats
        transitions = dfa_config['transitions']
        if isinstance(transitions, list):
            # Convert from list format to dictionary
            transition_dict = {}
            for transition in transitions:
                if len(transition) != 3:
                    return jsonify({
                        'success': False, 
                        'error': f'Invalid transition format: {transition}. Expected [from, symbol, to]'
                    }), 400
                from_state, symbol, to_state = transition
                transition_dict[(from_state, symbol)] = to_state
            transitions = transition_dict
        elif isinstance(transitions, dict):
            # Handle string keys from JSON (convert back to tuples)
            transition_dict = {}
            for key, value in transitions.items():
                if isinstance(key, str) and ',' in key:
                    # Handle "state,symbol" format
                    parts = key.split(',', 1)  # Split only on first comma
                    if len(parts) == 2:
                        from_state, symbol = parts[0].strip(), parts[1].strip()
                        transition_dict[(from_state, symbol)] = value
                    else:
                        return jsonify({
                            'success': False, 
                            'error': f'Invalid transition key format: {key}'
                        }), 400
                else:
                    return jsonify({
                        'success': False, 
                        'error': f'Invalid transition format: {key}'
                    }), 400
            transitions = transition_dict
        
        # Create DFA from configuration
        dfa = DFA(
            states=set(dfa_config['states']),
            alphabet=set(dfa_config['alphabet']),
            transitions=transitions,
            start_state=dfa_config['start_state'],
            accept_states=set(dfa_config['accept_states'])
        )
        
        # Simulate
        result = dfa.simulate(input_string)
        
        return jsonify({
            'success': True,
            'accepted': result['accepted'],
            'path': result['path'],
            'final_state': result['final_state']
        })
        
    except Exception as e:
        app.logger.error(f"Simulation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/minimize', methods=['POST'])
def api_minimize():
    """API endpoint for DFA minimization"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        dfa_config = data.get('dfa')
        
        if not dfa_config:
            return jsonify({'success': False, 'error': 'DFA configuration is required'}), 400
        
        # Validate DFA configuration (same as simulation)
        required_fields = ['states', 'alphabet', 'transitions', 'start_state', 'accept_states']
        for field in required_fields:
            if field not in dfa_config:
                return jsonify({
                    'success': False, 
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate limits
        max_states = app.config.get('MAX_STATES', 100)
        max_alphabet = app.config.get('MAX_ALPHABET_SIZE', 20)
        
        if len(dfa_config['states']) > max_states:
            return jsonify({
                'success': False, 
                'error': f'Too many states (max {max_states})'
            }), 400
        
        if len(dfa_config['alphabet']) > max_alphabet:
            return jsonify({
                'success': False, 
                'error': f'Alphabet too large (max {max_alphabet} symbols)'
            }), 400
        
        # Process transitions - handle both list and dict formats
        transitions = dfa_config['transitions']
        if isinstance(transitions, list):
            # Convert from list format to dictionary
            transition_dict = {}
            for transition in transitions:
                if len(transition) != 3:
                    return jsonify({
                        'success': False, 
                        'error': f'Invalid transition format: {transition}. Expected [from, symbol, to]'
                    }), 400
                from_state, symbol, to_state = transition
                transition_dict[(from_state, symbol)] = to_state
            transitions = transition_dict
        elif isinstance(transitions, dict):
            # Handle string keys from JSON (convert back to tuples)
            transition_dict = {}
            for key, value in transitions.items():
                if isinstance(key, str) and ',' in key:
                    # Handle "state,symbol" format
                    parts = key.split(',', 1)  # Split only on first comma
                    if len(parts) == 2:
                        from_state, symbol = parts[0].strip(), parts[1].strip()
                        transition_dict[(from_state, symbol)] = value
                    else:
                        return jsonify({
                            'success': False, 
                            'error': f'Invalid transition key format: {key}'
                        }), 400
                else:
                    return jsonify({
                        'success': False, 
                        'error': f'Invalid transition format: {key}'
                    }), 400
            transitions = transition_dict
        
        # Create DFA from configuration
        dfa = DFA(
            states=set(dfa_config['states']),
            alphabet=set(dfa_config['alphabet']),
            transitions=transitions,
            start_state=dfa_config['start_state'],
            accept_states=set(dfa_config['accept_states'])
        )
        
        # Minimize DFA
        minimizer = DFAMinimizer()
        minimized_dfa = minimizer.minimize(dfa)
        
        # Convert transitions back to JSON-serializable format
        transitions_list = []
        for (from_state, symbol), to_state in minimized_dfa.transitions.items():
            transitions_list.append([from_state, symbol, to_state])
        
        return jsonify({
            'success': True,
            'original_states': len(dfa.states),
            'minimized_states': len(minimized_dfa.states),
            'minimized_dfa': {
                'states': list(minimized_dfa.states),
                'alphabet': list(minimized_dfa.alphabet),
                'transitions': transitions_list,
                'start_state': minimized_dfa.start_state,
                'accept_states': list(minimized_dfa.accept_states)
            }
        })
        
    except Exception as e:
        app.logger.error(f"Minimization error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/examples')
def api_examples():
    """Get list of example DFAs"""
    examples_dir = os.path.join(app.root_path, 'examples')
    examples = []
    
    for filename in os.listdir(examples_dir):
        if filename.endswith('.json'):
            examples.append(filename)
    
    return jsonify({'examples': examples})

@app.route('/api/examples/<filename>')
def api_load_example(filename):
    """Load a specific example DFA"""
    try:
        filepath = os.path.join(app.root_path, 'examples', filename)
        dfa_config = load_dfa_from_json(filepath)
        return jsonify({'success': True, 'dfa': dfa_config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'], 
        host=app.config['HOST'], 
        port=app.config['PORT']
    )
