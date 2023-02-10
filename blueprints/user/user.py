import os
import requests
from urllib.parse import urlencode
from flask import Blueprint, redirect, request

bp_user = Blueprint("Users", __name__, url_prefix="/")

@bp_user.route("/get/users", methods=['GET', 'POST'])
def get_users():
    id = '1'
    name = 'Henrique'
    token = 'token'
    return {
        'id': id,
        'name': name,
        'token': token
    }

@bp_user.route("users/authorize", methods=['GET'])
def authorize():

    # check if request is a google callback
    url_params = request.args
    if url_params.get('code'):
        return {
            'authorization_code': url_params['code']
        }

    # redirect authorization to google
    params = {
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "scope": 'profile https://www.googleapis.com/auth/gmail.send',
        "include_granted_scopes": 'true',
        "response_type": 'code',
        "access_type": 'offline',
        "redirect_uri": 'http://localhost:5000/users/authorize'
    }

    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
    return redirect(location=url)