from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('index', __name__)

@bp.route('/')
def serve_index():
    if g.user is not None:
        return redirect('/servers', 302)

    return render_template('index.html')