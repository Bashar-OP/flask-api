from flask import  request, jsonify
from controllers.user_controller import *
import http_status as status
from routes.init import main



@main.route('/user')
def list_users():
    try:
        users = get_users()

        if not users:
            return jsonify("No users found"), status.HTTP_NOT_FOUND

        return jsonify([u.to_dict() for u in users]), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR

@main.route('/user/<int:id>')
def get_user(id: int):
    try:
        users = get_users(id)

        if not users:
            return jsonify("User not found"), status.HTTP_NOT_FOUND

        return jsonify(users[0].to_dict()), status.HTTP_OK

    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/user', methods=['POST'])
def add_user_route():
    try:
        data = {'name':request.form.get("name"),
        'library_id':request.form.get("library_id", type=int)
        }

        errors = []

        errors = validate_user_data(data)
        if errors:
            return jsonify({"errors":errors}), status.HTTP_BAD_REQUEST
        else:
            new_user = add_user(data)
            return jsonify(new_user.to_dict()), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/user/<int:id>', methods=['DELETE'])
def delete_user_route(id):
    try:
        deleted_user = delete_user(id)
        if deleted_user is None:
            return jsonify("User not found"), status.HTTP_NOT_FOUND
        
        return jsonify(f'user {deleted_user.id} deleted') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/user/<int:id>', methods=['PATCH'])
def update_user_route(id):
    try:
        data = {
            'name': request.form.get('name'),
            'library_id': request.form.get('library_id', type=int)
        }

        errors = validate_user_data(data,mode="update")
        if errors:
            return jsonify({"errors": errors}), status.HTTP_BAD_REQUEST

        updated_user = update_user(id,data)
        if updated_user is None:
            return jsonify("User not found"), status.HTTP_NOT_FOUND

        return jsonify(f'user {updated_user.id} updated') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR
    
