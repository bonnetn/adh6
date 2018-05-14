from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from .models import db, User, OAuth2Client
from .oauth2 import authorization, require_oauth
# from authlib.specs.rfc6749 import OAuth2Error
from website.ldap import LdapServ


bp = Blueprint(__name__, 'home')


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@bp.route('/logout')
def logout():
    del session['id']
    return redirect(request.referrer)


@bp.route('/create_client', methods=('GET', 'POST'))
def create_client():
    user = current_user()
    if not user:
        return redirect(url_for('website.routes.home'))
    if request.method == 'GET':
        return render_template('create_client.html')
    client = OAuth2Client(**request.form.to_dict(flat=True))
    client.user_id = user.id
    client.client_id = gen_salt(24)
    if client.token_endpoint_auth_method == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)
    db.session.add(client)
    db.session.commit()
    return redirect(url_for('website.routes.home'))


def ask_for_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        if not user.check_password(password):
            return redirect(url_for("website.routes.authorize"))

        session['id'] = user.id
        return None

    elif request.method == 'GET':
        user = current_user()
        return render_template('home.html', user=user, clients=[])


@bp.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    if not user:
        returnVal = ask_for_login()
        if returnVal:
            return returnVal

    grant_user = current_user()
    return authorization.create_authorization_response(grant_user=grant_user)


@bp.route('/api/me')
@require_oauth('profile')
def api_me():
    user = current_token.user

    groups = LdapServ.find_groups(user.username)
    adh6_groups = []

    if "adh6_user" in groups:
        adh6_groups += ["adh6_user"]

    if "adh6_admin" in groups:
        adh6_groups += ["adh6_admin"]

    return jsonify({
        "uid": user.username,
        "groups": adh6_groups
    })
