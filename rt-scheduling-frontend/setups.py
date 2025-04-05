from flask import (
    Blueprint, render_template, request, jsonify, flash
)
import os
import json
import uuid

bp = Blueprint('setups', __name__, url_prefix='/setups')


@bp.route('/', methods=['GET', 'POST'])
def list_setups():
    if request.method == 'GET':
        return render_template('/sim/setup/list_setups.html')


@bp.route('/new', methods=['GET', 'POST'])
def create_setup():
    if request.method == 'GET':
        return render_template('/sim/setup/create_setup.html')
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                # https://flask.palletsprojects.com/en/stable/patterns/flashing/#flashing-with-categories
                #TODO add error handling
                flash('No JSON data was recieved!')

            # Define the folder path for storing JSON files
            folder_path = os.path.join(os.getcwd(), 'data/sim_setup_files')
            
            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path for the JSON file
            save_path = os.path.join(folder_path, f"rt-scheduling-simulator-setup_{uuid.uuid4()}.json")
            
            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            return render_template('/sim/result.html')

        except Exception as e:
            #TODO add error handling
            return jsonify({'error': str(e)}), 500