from flask import Blueprint

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