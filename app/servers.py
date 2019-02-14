from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from app.auth import login_required
from app.db import get_db

bp = Blueprint('servers', __name__)

@bp.route('/servers')
def get_servers():
    db = get_db()
    server_list = db.execute(
        'SELECT * FROM servers'
    ).fetchall()

    return render_template('servers.html', server_list=server_list)