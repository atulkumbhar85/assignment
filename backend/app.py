from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# JSON file path for storing data
DATA_FILE = 'todolist.json'

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return "Flask backend is running."

@app.route('/process', methods=['POST'])
def submittodoitem():
    """Handle to-do item creation and save to JSON file"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        item_name = data.get('item_name')
        item_description = data.get('item_description')

        # Validate input
        if not item_name or not item_description:
            return jsonify({
                'success': False,
                'message': 'Item name and description are required'
            }), 400

        # Load existing data
        todolist = load_data()

        # Create new item
        new_item = {
            'item_id': len(todolist) + 1,
            'item_name': item_name,
            'item_description': item_description,
        }

        # Add to list and save
        todolist.append(new_item)
        save_data(todolist)

        return jsonify({
            'success': True,
            'message': 'To-Do item added successfully',
            'item_id': new_item['item_id']
        })
    except Exception as e:
        print(f"Error in submittodoitem: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/api/todolist', methods=['GET'])
def get_todolist():
    """Retrieve the list of to-do items"""
    try:
        todolist = load_data()
        return jsonify({
            'success': True,
            'todolist': todolist
        })
    except Exception as e:
        print(f"Error in get_todolist: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

if __name__ == '__main__':
    print("Starting Flask backend server...")
    app.run(debug=True, host='0.0.0.0', port=5000)