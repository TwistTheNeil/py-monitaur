from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('index', __name__)

@bp.route('/')
def serve_index():
    return render_template('index.html')