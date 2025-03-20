from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('sim', __name__, url_prefix='/sim')

@bp.route('taskset', methods=['Get'])
def taskset():
    if request.method == 'GET':
        return render_template('/sim/setup.html')

@bp.route('result', methods=['Get'])
def result():
    if request.method == 'GET':
        return render_template('/sim/result.html')
