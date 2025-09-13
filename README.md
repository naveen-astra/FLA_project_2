# DFA Minimizer Web Application

A comprehensive web application for working with Deterministic Finite Automata (DFA), including simulation and minimization using Hopcroft's algorithm.

## Features

- **DFA Simulation**: Test input strings against your DFA to see if they are accepted
- **DFA Minimization**: Reduce DFA to its minimal equivalent form using Hopcroft's algorithm
- **Interactive Web Interface**: User-friendly web interface built with Flask
- **Example DFAs**: Pre-loaded example DFAs to get started quickly
- **JSON Support**: Import and export DFA configurations
- **Comprehensive Testing**: Unit tests for all core functionality
- **Visual Results**: Clear transition tables and simulation paths

## Project Structure

```
dfa_minimizer_webapp/
├── app.py                        # Main Flask application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── dfa/                          # Core DFA logic
│   ├── __init__.py
│   ├── dfa.py                    # DFA class implementation
│   ├── minimizer.py              # Hopcroft's algorithm
│   └── utils.py                  # Utility functions
├── static/                       # Static web assets
│   ├── css/style.css            # Application styling
│   ├── js/script.js             # Client-side JavaScript
│   └── images/logo.png          # Project logo
├── templates/                    # HTML templates
│   ├── base.html                # Base template
│   ├── index.html               # Home page
│   ├── simulate.html            # DFA simulation page
│   └── minimize.html            # DFA minimization page
├── examples/                     # Example DFA configurations
│   ├── sample_dfa1.json         # Simple DFA example
│   └── sample_dfa2.json         # DFA with redundant states
└── tests/                       # Unit tests
    ├── test_dfa.py              # Tests for DFA class
    └── test_minimizer.py        # Tests for minimizer
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download** the project to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd dfa_minimizer_webapp
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

### Using the Web Interface

#### DFA Simulation
1. Go to the "Simulate" page
2. Define your DFA by entering:
   - States (comma-separated): `q0, q1, q2`
   - Alphabet (comma-separated): `0, 1`
   - Start state: `q0`
   - Accept states (comma-separated): `q2`
   - Transitions (one per line): `q0,0,q1`
3. Enter an input string to test
4. Click "Simulate" to see the result

#### DFA Minimization
1. Go to the "Minimize" page
2. Define your DFA using the same format as simulation
3. Click "Minimize DFA" to see the reduced DFA
4. Compare the original and minimized versions

#### Loading Examples
- Both simulation and minimization pages have dropdown menus to load example DFAs
- Select an example to automatically populate the form fields

## DFA Input Format

### States and Alphabet
Enter comma-separated values:
```
States: q0, q1, q2, q3
Alphabet: 0, 1, a, b
```

### Transitions
Enter one transition per line in the format `from_state,symbol,to_state`:
```
q0,0,q1
q0,1,q0
q1,0,q2
q1,1,q0
```

### JSON Format
DFA configurations can also be stored as JSON:
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["0", "1"],
  "transitions": [
    ["q0", "0", "q1"],
    ["q0", "1", "q0"],
    ["q1", "0", "q1"],
    ["q1", "1", "q2"],
    ["q2", "0", "q1"],
    ["q2", "1", "q0"]
  ],
  "start_state": "q0",
  "accept_states": ["q2"]
}
```

## API Endpoints

The application provides REST API endpoints:

- `POST /api/simulate` - Simulate DFA with input string
- `POST /api/minimize` - Minimize DFA using Hopcroft's algorithm
- `GET /api/examples` - Get list of example DFAs
- `GET /api/examples/<filename>` - Load specific example DFA

## Examples

### Example 1: Binary Strings Ending in "01"
This DFA accepts binary strings that end with "01":

**Configuration:**
- States: q0, q1, q2
- Alphabet: 0, 1
- Start State: q0
- Accept States: q2

**Transitions:**
```
q0,0,q1
q0,1,q0
q1,0,q1
q1,1,q2
q2,0,q1
q2,1,q0
```

**Test Cases:**
- "01" → ACCEPTED
- "101" → ACCEPTED
- "1001" → ACCEPTED
- "10" → REJECTED
- "11" → REJECTED

### Example 2: DFA with Redundant States
This example demonstrates a DFA that can be minimized by merging equivalent states.

## Testing

Run the unit tests to verify functionality:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_dfa.py

# Run with verbose output
python -m pytest tests/ -v
```

### Test Coverage
- DFA class functionality
- DFA validation and error handling
- Simulation with various input strings
- Hopcroft's minimization algorithm
- Equivalent state detection
- Unreachable state removal

## Algorithm Details

### Hopcroft's Algorithm
The minimization uses Hopcroft's algorithm, which:

1. **Initial Partitioning**: Separates states into accepting and non-accepting
2. **Refinement**: Iteratively splits partitions based on transition behavior
3. **Convergence**: Continues until no further refinement is possible
4. **Construction**: Builds minimal DFA from final partitions

**Time Complexity**: O(kn log n) where k is alphabet size and n is number of states

### DFA Validation
The application validates:
- All states are properly defined
- Start state exists in state set
- Accept states are subset of all states
- Transitions reference valid states and symbols
- No undefined transitions during simulation

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

2. **Port Already in Use**: If port 5000 is busy, modify `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

3. **Invalid DFA Configuration**: Check that:
   - All state names are consistent
   - Transitions reference existing states
   - Start state is in the state set
   - Accept states are subset of all states

4. **Browser Compatibility**: Use modern browsers (Chrome, Firefox, Safari, Edge)

### Error Messages
- **"Symbol not in alphabet"**: Input string contains undefined symbols
- **"No transition from state"**: DFA is incomplete for given input
- **"Start state not in states"**: Start state is not properly defined
- **"Accept states must be subset"**: Accept states reference undefined states

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Educational Use

This application is designed for educational purposes in:
- **Formal Language Theory**: Understanding DFA concepts
- **Automata Theory**: Learning about finite state machines
- **Algorithm Analysis**: Studying Hopcroft's minimization algorithm
- **Web Development**: Flask application structure and design

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Based on Hopcroft's DFA minimization algorithm
- Built with Flask web framework
- Designed for computer science education
- Inspired by formal language and automata theory coursework

## Contact

For questions, issues, or contributions, please refer to the project repository or course materials.
