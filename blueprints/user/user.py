import json
from flask import Blueprint, request
import google_auth_oauthlib
from requests import HTTPError
from exceptions.NetworkException import NetworkException
import flask

from services.auth.AuthService import AuthService
from services.auth.dto.GoogleAuthDto import GoogleAuthDto

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

@bp_user.route("/get/token", methods=['POST', 'GET'])
def get_token():
    args = request.args
    state = args.get('state')
    code = args.get('code')
    authorization_code = args.get('authorization_code')
    auth_service = AuthService()

    auth_dto : GoogleAuthDto = auth_service.get_token(authorization_code=code)

    return auth_dto.to_dict(), 200


@bp_user.route('users/authorize', methods=['GET', 'POST'])
def authorize():
    auth_service = AuthService()

    # check if request is a google callback
    url_params = request.args
    if url_params.get('code'):
        auth_dto = GoogleAuthDto(authorization_code=url_params['code'])
        return json.dumps(obj=auth_dto.__dict__,
                          sort_keys=False)
    
    # request authorization
    return auth_service.authorize()
    
@bp_user.route('users/token', methods=['POST'])
def update_token():
    try:
        auth_service = AuthService()

        data = request.get_json()

        authorization_code = data.get('authorization_code') or ''
        if not authorization_code:
            return "Required param 'authorization_code' was not provided", 400
        
        auth_dto : GoogleAuthDto = auth_service.get_token(authorization_code=authorization_code)
        return auth_dto.to_dict(), 200

    except NetworkException as e:
        return json.dumps(obj=e.__dict__, sort_keys=False), e.status_code

    except Exception as e:
        error_payload = {"error": e.args[0]} if e.args[0] else None
        if not error_payload:
             raise e
        
        return error_payload, 500
    
@bp_user.route('/revoke', methods=['POST'])
def revoke():
    auth_service = AuthService()

    data = request.json
    token = data.get('token')

    revoke = auth_service.revoke(token=token)
    message = json.loads(revoke.text)

    return {
        'status_code': revoke.status_code,
        'message': message
    }
