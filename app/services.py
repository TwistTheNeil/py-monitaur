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
        'select S.name as name, S.id as id, MAX(L.logged_at) as last_seen from services S, logged_times L, servers R where S.id = L.service_id and R.id = ? group by S.name',
        (id,)
    ).fetchall()

    return json.dumps([dict(x) for x in data])

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