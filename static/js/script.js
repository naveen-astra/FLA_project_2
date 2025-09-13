// DFA Minimizer Web App JavaScript

class DFAApp {
    constructor() {
        this.currentDFA = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadExamples();
    }

    setupEventListeners() {
        // Example loading
        const exampleSelect = document.getElementById('exampleSelect');
        if (exampleSelect) {
            exampleSelect.addEventListener('change', (e) => {
                if (e.target.value) {
                    this.loadExample(e.target.value);
                }
            });
        }

        // DFA simulation
        const simulateBtn = document.getElementById('simulateBtn');
        if (simulateBtn) {
            simulateBtn.addEventListener('click', () => this.simulateDFA());
        }

        // DFA minimization
        const minimizeBtn = document.getElementById('minimizeBtn');
        if (minimizeBtn) {
            minimizeBtn.addEventListener('click', () => this.minimizeDFA());
        }

        // Clear buttons
        const clearBtns = document.querySelectorAll('.clear-btn');
        clearBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetId = e.target.dataset.target;
                if (targetId) {
                    document.getElementById(targetId).value = '';
                }
            });
        });
    }

    async loadExamples() {
        try {
            const response = await fetch('/api/examples');
            const data = await response.json();
            
            const select = document.getElementById('exampleSelect');
            if (select && data.examples) {
                data.examples.forEach(example => {
                    const option = document.createElement('option');
                    option.value = example;
                    option.textContent = example.replace('.json', '').replace('_', ' ');
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading examples:', error);
        }
    }

    async loadExample(filename) {
        try {
            const response = await fetch(`/api/examples/${filename}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentDFA = data.dfa;
                this.populateDFAForm(data.dfa);
                this.showAlert('Example loaded successfully!', 'success');
            } else {
                this.showAlert(`Error loading example: ${data.error}`, 'error');
            }
        } catch (error) {
            this.showAlert(`Error loading example: ${error.message}`, 'error');
        }
    }

    populateDFAForm(dfa) {
        // Populate form fields with DFA data
        const statesInput = document.getElementById('states');
        const alphabetInput = document.getElementById('alphabet');
        const transitionsInput = document.getElementById('transitions');
        const startStateInput = document.getElementById('startState');
        const acceptStatesInput = document.getElementById('acceptStates');

        if (statesInput) statesInput.value = dfa.states.join(', ');
        if (alphabetInput) alphabetInput.value = dfa.alphabet.join(', ');
        if (startStateInput) startStateInput.value = dfa.start_state;
        if (acceptStatesInput) acceptStatesInput.value = dfa.accept_states.join(', ');
        
        if (transitionsInput) {
            const transitionStrings = [];
            
            if (Array.isArray(dfa.transitions)) {
                // Handle list format: [[from, symbol, to], ...]
                for (const transition of dfa.transitions) {
                    if (transition.length === 3) {
                        transitionStrings.push(`${transition[0]},${transition[1]},${transition[2]}`);
                    }
                }
            } else if (typeof dfa.transitions === 'object') {
                // Handle object format: {"state,symbol": "to_state", ...}
                for (const [key, value] of Object.entries(dfa.transitions)) {
                    if (key.includes(',')) {
                        const [state, symbol] = key.split(',', 2);
                        transitionStrings.push(`${state.trim()},${symbol.trim()},${value}`);
                    }
                }
            }
            
            transitionsInput.value = transitionStrings.join('\n');
        }
    }

    getDFAFromForm() {
        const states = this.parseCommaSeparated(document.getElementById('states').value);
        const alphabet = this.parseCommaSeparated(document.getElementById('alphabet').value);
        const startState = document.getElementById('startState').value.trim();
        const acceptStates = this.parseCommaSeparated(document.getElementById('acceptStates').value);
        const transitionsText = document.getElementById('transitions').value.trim();

        // Validate basic inputs
        if (states.length === 0) {
            throw new Error('At least one state is required');
        }
        
        if (alphabet.length === 0) {
            throw new Error('Alphabet cannot be empty');
        }
        
        if (!startState) {
            throw new Error('Start state is required');
        }
        
        if (!states.includes(startState)) {
            throw new Error('Start state must be in the set of states');
        }

        // Parse transitions
        const transitions = {};
        if (transitionsText) {
            const lines = transitionsText.split('\n');
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i].trim();
                if (line) {
                    const parts = line.split(',');
                    if (parts.length !== 3) {
                        throw new Error(`Invalid transition format on line ${i + 1}: "${line}". Use format: from,symbol,to`);
                    }
                    const [from, symbol, to] = parts.map(p => p.trim());
                    
                    // Validate transition components
                    if (!states.includes(from)) {
                        throw new Error(`Unknown state "${from}" in transition on line ${i + 1}`);
                    }
                    if (!alphabet.includes(symbol)) {
                        throw new Error(`Unknown symbol "${symbol}" in transition on line ${i + 1}`);
                    }
                    if (!states.includes(to)) {
                        throw new Error(`Unknown state "${to}" in transition on line ${i + 1}`);
                    }
                    
                    transitions[`${from},${symbol}`] = to;
                }
            }
        }

        // Validate accept states
        for (const acceptState of acceptStates) {
            if (!states.includes(acceptState)) {
                throw new Error(`Accept state "${acceptState}" must be in the set of states`);
            }
        }

        return {
            states,
            alphabet,
            transitions,
            start_state: startState,
            accept_states: acceptStates
        };
    }

    parseCommaSeparated(value) {
        return value.split(',').map(item => item.trim()).filter(item => item.length > 0);
    }

    async simulateDFA() {
        try {
            // Validate DFA input first
            this.validateDFAInput();
            
            const dfa = this.getDFAFromForm();
            const inputString = document.getElementById('inputString').value;

            this.showLoading('simulateBtn');

            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    dfa: dfa,
                    input_string: inputString
                })
            });

            const data = await response.json();
            this.hideLoading('simulateBtn');

            if (data.success) {
                this.displaySimulationResult(data);
            } else {
                this.showAlert(`Simulation error: ${data.error}`, 'error');
            }
        } catch (error) {
            this.hideLoading('simulateBtn');
            this.showAlert(`Error: ${error.message}`, 'error');
        }
    }

    async minimizeDFA() {
        try {
            // Validate DFA input first
            this.validateDFAInput();
            
            const dfa = this.getDFAFromForm();

            this.showLoading('minimizeBtn');

            const response = await fetch('/api/minimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    dfa: dfa
                })
            });

            const data = await response.json();
            this.hideLoading('minimizeBtn');

            if (data.success) {
                this.displayMinimizationResult(data);
            } else {
                this.showAlert(`Minimization error: ${data.error}`, 'error');
            }
        } catch (error) {
            this.hideLoading('minimizeBtn');
            this.showAlert(`Error: ${error.message}`, 'error');
        }
    }

    displaySimulationResult(result) {
        const resultDiv = document.getElementById('simulationResult');
        if (!resultDiv) return;

        const status = result.accepted ? 'ACCEPTED' : 'REJECTED';
        const statusClass = result.accepted ? 'accepted' : 'rejected';
        
        let pathHtml = '';
        if (result.path && result.path.length > 0) {
            pathHtml = result.path.map(state => 
                `<span class="state-highlight">${state}</span>`
            ).join(' → ');
        }

        resultDiv.innerHTML = `
            <div class="simulation-path">
                <h4>Simulation Result: <span class="${statusClass}">${status}</span></h4>
                <p><strong>Final State:</strong> ${result.final_state}</p>
                <p><strong>Path:</strong> ${pathHtml}</p>
                ${result.error ? `<p class="alert alert-error">${result.error}</p>` : ''}
            </div>
        `;

        resultDiv.classList.remove('hidden');
    }

    displayMinimizationResult(result) {
        const resultDiv = document.getElementById('minimizationResult');
        if (!resultDiv) return;

        const dfa = result.minimized_dfa;
        
        resultDiv.innerHTML = `
            <div class="card">
                <h4>Minimization Result</h4>
                <p><strong>Original States:</strong> ${result.original_states}</p>
                <p><strong>Minimized States:</strong> ${result.minimized_states}</p>
                <p><strong>Reduction:</strong> ${result.original_states - result.minimized_states} states removed</p>
                
                <h5>Minimized DFA:</h5>
                <div class="dfa-container">
                    <p><strong>States:</strong> {${dfa.states.join(', ')}}</p>
                    <p><strong>Alphabet:</strong> {${dfa.alphabet.join(', ')}}</p>
                    <p><strong>Start State:</strong> ${dfa.start_state}</p>
                    <p><strong>Accept States:</strong> {${dfa.accept_states.join(', ')}}</p>
                    
                    <h6>Transition Table:</h6>
                    ${this.createTransitionTable(dfa)}
                </div>
            </div>
        `;

        resultDiv.classList.remove('hidden');
    }

    createTransitionTable(dfa) {
        let table = '<table class="transition-table"><thead><tr><th>State</th>';
        
        // Header row
        for (const symbol of dfa.alphabet) {
            table += `<th>${symbol}</th>`;
        }
        table += '</tr></thead><tbody>';

        // Convert transitions to lookup object if it's in list format
        let transitionLookup = {};
        if (Array.isArray(dfa.transitions)) {
            for (const [from, symbol, to] of dfa.transitions) {
                transitionLookup[`${from},${symbol}`] = to;
            }
        } else {
            transitionLookup = dfa.transitions;
        }

        // Data rows
        for (const state of dfa.states) {
            table += `<tr><td><strong>${state}</strong></td>`;
            for (const symbol of dfa.alphabet) {
                const key = `${state},${symbol}`;
                const nextState = transitionLookup[key] || '-';
                table += `<td>${nextState}</td>`;
            }
            table += '</tr>';
        }

        table += '</tbody></table>';
        return table;
    }

    showLoading(buttonId) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.disabled = true;
            button.innerHTML = '<span class="loading"></span> Processing...';
        }
    }

    hideLoading(buttonId) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.disabled = false;
            // Restore original text based on button type
            if (buttonId === 'simulateBtn') {
                button.innerHTML = 'Simulate';
            } else if (buttonId === 'minimizeBtn') {
                button.innerHTML = 'Minimize DFA';
            }
        }
    }

    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        // Insert at top of main content
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(alertDiv, main.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 5000);
        }
    }

    // Utility method to validate DFA input
    validateDFAInput() {
        const dfa = this.getDFAFromForm();
        
        if (!dfa.states.length) {
            throw new Error('States cannot be empty');
        }
        
        if (!dfa.alphabet.length) {
            throw new Error('Alphabet cannot be empty');
        }
        
        if (!dfa.start_state) {
            throw new Error('Start state cannot be empty');
        }
        
        if (!dfa.states.includes(dfa.start_state)) {
            throw new Error('Start state must be in the set of states');
        }
        
        for (const acceptState of dfa.accept_states) {
            if (!dfa.states.includes(acceptState)) {
                throw new Error(`Accept state '${acceptState}' must be in the set of states`);
            }
        }
        
        return true;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DFAApp();
});

// Utility functions for form handling
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.toggle('hidden');
    }
}

function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}
