from flask import jsonify, session, Blueprint, redirect, url_for
from app.auth.utils import (auth0, requires_auth, user_is_logged_in,
                            clear_user_session_keys)
from app.serve import CLIENT_ID, REDIRECT_AUDIENCE, REDIRECT_URI
from six.moves.urllib.parse import urlencode

from app.users.utils import maybe_add_user
from app.users.controllers import users

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.route('/callback', methods=['GET'])
def callback_handling():
    """Handles response from token endpoint to get the userinfo"""
    token = auth0.authorize_access_token()
    print(token)
    session['token'] = token['id_token']
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    res = maybe_add_user(userinfo['name'], userinfo['picture'],
                          userinfo['sub'])
    if res:
        return jsonify(success=False, error=str(res))
    return redirect(url_for('auth.api_private'))


@auth.route('/login', methods=['GET'])
def login():
    """Access the login page"""
    return auth0.authorize_redirect(
        redirect_uri=REDIRECT_URI, audience=REDIRECT_AUDIENCE)


@auth.route('/logout', methods=['GET'])
@user_is_logged_in
def logout():
    """Removes user login details from session, logging out the user"""
    clear_user_session_keys()
    # TODO: Handle error messages for this function
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('auth.api_public', _external=True),
        'client_id': CLIENT_ID
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@auth.route('/public', methods=['GET', 'POST'])
def api_public():
    """
        Route that requires no authentication.
    """
    return jsonify(message="Public route with no auth")


@auth.route('/private', methods=['GET', 'POST'])
@requires_auth
def api_private():
    """
        Route that requires authentication.
        Used for redirecting once user is logged in and validated.
        Information will be stored for validation for other routes.
    """
    return jsonify(message="Private route with auth")
