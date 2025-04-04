from flask import (
    Blueprint, render_template, request, jsonify, flash
)
import os
import json

bp = Blueprint('sim', __name__, url_prefix='/sim')

@bp.route('taskset', methods=['GET', 'POST'])
def taskset():
    if request.method == 'GET':
        return render_template('/sim/setup.html')
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                flash('No JSON data was recieved!')
                #TODO add error handling

            # Define the folder path for storing JSON files
            folder_path = os.path.join(os.getcwd(), 'rt-scheduling-simulator/sim_setup_files')
            
            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path for the JSON file
            save_path = os.path.join(folder_path, 'received_data.json')
            
            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            return render_template('/sim/result.html')

        except Exception as e:
            #TODO add error handling
            return jsonify({'error': str(e)}), 500

@bp.route('result', methods=['GET'])
def result():
    if request.method == 'GET':
        return render_template('/sim/result.html')
