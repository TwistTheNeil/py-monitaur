from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import datetime
import uuid
import json

from app.auth import login_required
from app.db import get_db
from app.helpers import create_new_uuid

bp = Blueprint('servers', __name__)

@bp.route('/servers')
@login_required
def get_servers():
    return render_template('servers.html')

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
        'select S.name as name, S.id as id, MAX(L.logged_at) as last_logged from servers S, logged_times L where S.id = L.server_id group by S.id'
    ).fetchall()

    return json.dumps([dict(x) for x in server_list])

@bp.route('/servers/<id>/ping', methods=['POST'])
def ping_server(id):
    db = get_db()
    db.execute(
        'insert into logged_times (server_id) values (?)',
        (id,)
    )
    db.commit()

    return jsonify(
        err=""
    )

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

        db.execute(
            'insert into logged_times (server_id, logged_at) values (?, ?)',
            (str(new_server_id),0,)
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