from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('', methods=['Get'])
def home():
    if request.method == 'GET':
        return render_template('/home/home.html')
