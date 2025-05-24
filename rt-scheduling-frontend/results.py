from flask import (
    Blueprint, abort, redirect, render_template, request, send_from_directory, url_for
)
import os
import json

bp = Blueprint('results', __name__, url_prefix='/results')
# Define the folder path for storing JSON files
setup_folder_path = os.path.join(os.getcwd(), 'data/sim_setup_files')
result_folder_path = os.path.join(os.getcwd(), 'data/sim_result_files')


@bp.route('/', methods=['GET']) # type: ignore
def list_results():
    if request.method == 'GET':
        filenames = []
        setupnames = []

        for filename in os.listdir(result_folder_path):
            filenames.append(filename)
            file_path = os.path.join(result_folder_path, filename)
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
def delete_result(filename):
    if request.method == 'DELETE':
        os.remove(f"{result_folder_path}/{filename}")
        
    return redirect(url_for('setups.list_setups'))

@bp.route('/download/<string:filename>', methods=['GET']) # type: ignore
def download_result(filename):
    if request.method == 'GET':
        try:
            return send_from_directory(result_folder_path, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)

@bp.route('/<string:result_id>', methods=['GET'])
def view_result(result_id: str):
    with open(f"{result_folder_path}/rt-scheduling-simulator-result_{result_id}.json") as f:
        data = json.load(f)
    return render_template("sim/result/result.html", chart_data=data)