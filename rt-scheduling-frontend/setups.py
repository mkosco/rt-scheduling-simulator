from flask import (
    Blueprint, abort, redirect, render_template, request, jsonify, flash, current_app, send_from_directory, url_for
)
import os
import json
import uuid
import subprocess

bp = Blueprint('setups', __name__, url_prefix='/setups')
# Define the folder path for storing JSON files
setup_folder_path = os.path.join(os.getcwd(), 'data/sim_setup_files')
result_folder_path = os.path.join(os.getcwd(), 'data/sim_result_files')


@bp.route('/', methods=['GET']) # type: ignore
def list_setups():
    if request.method == 'GET':
        filenames = []
        setupnames = []

        # Ensure the folder exists
        os.makedirs(setup_folder_path, exist_ok=True)

        for filename in os.listdir(setup_folder_path):
            filenames.append(filename)
            file_path = os.path.join(setup_folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'setup_name' in data:
                        setupnames.append(data['setup_name'])

        combined = [
            {'filename': f, 'setup_name': s}
            for f, s in zip(filenames, setupnames)
        ]
        return render_template('/sim/setup/list_setups.html', fileinfo=combined)

@bp.route('/delete/<string:filename>', methods=['DELETE']) # type: ignore
def delete_setup(filename):
    if request.method == 'DELETE':
        os.remove(f"{setup_folder_path}/{filename}")
        
    return redirect(url_for('setups.list_setups'))

@bp.route('/download/<string:filename>', methods=['GET']) # type: ignore
def download_setup(filename):
    if request.method == 'GET':
        try:
            return send_from_directory(setup_folder_path, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)


# TODO split this up into multiple functions and don't always automatically trigger sim, give the user the option
@bp.route('/new', methods=['GET', 'POST']) # type: ignore
def create_setup():
    if request.method == 'GET':
        return render_template('/sim/setup/create_setup.html')
    if request.method == 'POST':
        try:
            data = request.get_json()
            current_app.logger.debug(f"setup creation request data: {data}")

            if not data:
                flash('No JSON data was recieved!')
                return jsonify({'error': 'No JSON data was received!'}), 400

            current_app.logger.debug(data)
            current_app.logger.debug(f"folder path for sim setup file storage: {setup_folder_path}")
            
            # Ensure the folder exists
            os.makedirs(setup_folder_path, exist_ok=True)

            # Define the file path for the JSON file
            save_path = os.path.join(setup_folder_path, f"rt-scheduling-simulator-setup_{uuid.uuid4()}.json")
            current_app.logger.debug(f"folder path for the created sim setup file: {save_path}")

            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            simulation_package = 'rt_scheduling_simulator.simulation_runner'
            project_root = os.path.dirname(os.path.abspath("rt-scheduling-simulator"))  # Set to the root of the project
            print(f"project root: {project_root}")
            
            result = subprocess.run(
                ['python', '-m', simulation_package, save_path, "--debug"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            
            # Check the result of the subprocess
            if result.returncode != 0:
                current_app.logger.error(f"simulation runner failed: {result.stderr}")
            else:
                current_app.logger.debug(f"simulation subprocess: {result.stdout}")
            
            lines = result.stdout.splitlines()
            result_id = [line.strip() for line in lines][-1]

            url = url_for('results.view_result', result_id=result_id)
            return redirect(url)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500