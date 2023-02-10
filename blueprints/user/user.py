import json
from flask import Blueprint, request

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

@bp_user.route("users/authorize", methods=['GET'])
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
    
