from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

import json

from app.auth import login_required
from app.db import get_db
from app.helpers import create_new_uuid

bp = Blueprint('services', __name__)

@bp.route('/services/on/<id>')
@login_required
def show_services_page(id):
    name = get_db().execute(
        'select name from servers where id = ?',
        (id,)
    ).fetchone()['name']

    return render_template('services.html', server_name=name, server_id=id)

@bp.route('/services/on/<id>/list', methods=['GET'])
@login_required
def get_services(id):
    data = get_db().execute(
        'select S.name as name, S.id as id, MAX(L.logged_at) as last_seen, S.pinned, S.enabled from services S, logged_times L, servers R where S.id = L.service_id and S.server_id = ? group by S.name order by S.pinned desc',
        (id,)
    ).fetchall()

    return json.dumps([dict(x) for x in data])

@bp.route('/services/on/<id>/new', methods=['POST'])
@login_required
def new_service(id):
    new_service_name = request.form['registering-service-name']

    db = get_db()

    # Check if name exists
    result = db.execute(
        'select name from services where name = ?',
        (new_service_name,)
    ).fetchone()

    if result is None:
        new_service_id = create_new_uuid(new_service_name)

        db.execute(
            'insert into services (name, id, server_id) values (?, ?, ?)',
            (new_service_name, str(new_service_id), id)
        )
        db.commit()

        db.execute(
            'insert into logged_times (service_id, logged_at) values (?, ?)',
            (str(new_service_id),0,)
        )
        db.commit()

        return jsonify(
            name=new_service_name,
            id=new_service_id,
            last_seen="0",
            err=""
        )
    else:
        return jsonify(
            err="Server name already exists."
        )

# TODO: if a server has not been pinged, but a service has been,
# should the server be host server be marked as "up"?
@bp.route('/services/<id>/ping', methods=['POST'])
def ping_service(id):
    db = get_db()
    db.execute(
        'insert into logged_times (service_id) values (?)',
        (id,)
    )
    db.commit()

    return jsonify(
        err=""
    )

@bp.route('/services/<id>/remove', methods=['DELETE'])
@login_required
def remove_service(id):
    db = get_db()
    db.execute(
        'delete from services where id = ?',
        (id,)
    )
    db.commit()

    return jsonify(
        err=""
    )

@bp.route('/services/<id>/rename', methods=['PUT'])
@login_required
def rename_service(id):
    updated_name = request.form['updated_name']
    db = get_db()
    db.execute(
       'update services set name = ? where id = ?',
       (updated_name, id,)
    )
    db.commit()

    return jsonify(
        err=""
    )

@bp.route('/services/<id>/modpin', methods=['PUT'])
@login_required
def modify_service_pin_status(id):
    pin_status = request.form['pin_status']
    db = get_db()
    db.execute(
       'update services set pinned = ? where id = ?',
       (pin_status, id,)
    )
    db.commit()

    return jsonify(
        err=""
    )