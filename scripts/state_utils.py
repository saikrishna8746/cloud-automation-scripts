import json
import os

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'state.json')

def load_state():
    """Load the current state from state.json. Returns an empty dict if it doesn't exist."""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(state_dict):
    """Save the state dictionary to state.json."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state_dict, f, indent=4)

def update_state(key, value):
    """Update a specific key in the state file."""
    state = load_state()
    state[key] = value
    save_state(state)

def clear_state():
    """Clear the state file."""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
