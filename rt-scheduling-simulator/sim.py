from flask import (
    Blueprint, render_template, request
)
import json

bp = Blueprint('sim', __name__, url_prefix='/sim')

@bp.route('taskset', methods=['Get', 'Post'])
def taskset():
    if request.method == 'GET':
        return render_template('/sim/setup.html')
    if request.method == 'POST':
        form_data = request.form
        
        # Parse with type conversion
        parsed_data = {
            'resources_activated': form_data.get('resources_activated') == 'True',  # Convert to bool
            'algorithms': form_data.get('algorithms'),  # Already string
            'resources_hidden_input': json.loads(form_data.get('resources_hidden_input', '[]')),  # JSON to list
            'tasks_hidden_input': json.loads(form_data.get('tasks_hidden_input', '[]'))  # JSON to list of dicts
        }
        
        # Now you can work with properly typed data
        print(type(parsed_data['resources_activated']))  # bool
        print(type(parsed_data['algorithms']))  # str
        print(type(parsed_data['resources_hidden_input']))  # list
        print(type(parsed_data['tasks_hidden_input']))  # list of dicts        
        return render_template('/sim/setup.html')

@bp.route('result', methods=['Get'])
def result():
    if request.method == 'GET':
        return render_template('/sim/result.html')
