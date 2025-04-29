from flask import (
    Blueprint, render_template, request, jsonify, flash, current_app
)
import os
import json
import uuid
import subprocess

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
            current_app.logger.debug(f"setup creation request data: {data}")

            if not data:
                # https://flask.palletsprojects.com/en/stable/patterns/flashing/#flashing-with-categories
                #TODO add error handling
                flash('No JSON data was recieved!')

            # Define the folder path for storing JSON files
            folder_path = os.path.join(os.getcwd(), 'data/sim_setup_files')
            current_app.logger.debug(f"folder path for sim setup file storage: {folder_path}")
            
            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path for the JSON file
            save_path = os.path.join(folder_path, f"rt-scheduling-simulator-setup_{uuid.uuid4()}.json")
            current_app.logger.debug(f"folder path for the created sim setup file: {save_path}")

            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            simulation_package = 'rt-scheduling-simulator.simulation_runner'
            project_root = os.path.dirname(os.path.abspath("rt-scheduling-simulator"))  # Set to the root of the project
            print(f"project root: {project_root}")
            
            result = subprocess.run(
                ['python', '-m', simulation_package, save_path],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            # Check the result of the subprocess
            if result.returncode != 0:
                current_app.logger.error(f"simulation runner failed: {result.stderr}")
                flash(f"Simulation failed, check log")
            else:
                current_app.logger.debug(f"simulation subprocess: {result.stdout}")
                flash("Simulation ran successfully!")

                
            return render_template('/sim/result.html')

        except Exception as e:
            #TODO add error handling
            return jsonify({'error': str(e)}), 500