from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import datetime
import uuid
import json

from app.auth import login_required
from app.db import get_db

bp = Blueprint('servers', __name__)

@bp.route('/servers')
@login_required
def get_servers():
    return render_template('servers.html')

def create_new_uuid(server_name):
    return uuid.uuid3(
        uuid.NAMESPACE_DNS,
        server_name+datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    )

@bp.route('/servers/<name>/delete', methods=['POST'])
def remove_server(name):
    db = get_db()

    # TODO: delete respective services too
    db.execute(
        'delete from servers where name = ?',
        (name,)
    )
    db.commit()

    # TODO: Error?
    return jsonify(
        err=""
    )

@bp.route('/servers/list', methods=['GET'])
def list_servers():
    db = get_db()
    server_list = db.execute(
        'SELECT * FROM servers'
    ).fetchall()

    return json.dumps([dict(x) for x in server_list])

@bp.route('/servers/new', methods=['POST'])
def new_server():
    new_server_name = request.form['registering-server-name']

    db = get_db()

    # Check if name exists
    result = db.execute(
        'select name from servers where name = ?',
        (new_server_name,)
    ).fetchone()

    if result is None:
        new_server_id = create_new_uuid(new_server_name)

        db.execute(
            'insert into servers (name, id) values (?, ?)',
            (new_server_name, str(new_server_id))
        )
        db.commit()

        return jsonify(
            name=new_server_name,
            id=new_server_id,
            err=""
        )
    else:
        return jsonify(
            err="Server name already exists."
        )