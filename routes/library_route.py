from flask import  request, jsonify
from controllers.library_controller import *
import http_status as status
from routes.init import main



@main.route('/library')
def list_libraries():
    try:
        libraries = get_libraries()

        if not libraries:
            return jsonify("No libraries found"), status.HTTP_NOT_FOUND

        return jsonify([u.to_dict() for u in libraries]), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR

@main.route('/library/<int:id>')
def get_library(id: int):
    try:
        libraries = get_libraries(id)

        if not libraries:
            return jsonify("library not found"), status.HTTP_NOT_FOUND

        return jsonify(libraries[0].to_dict()), status.HTTP_OK

    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/library', methods=['POST'])
def add_library_route():
    try:
        data = {'name':request.form.get("name")
        }

        errors = []

        errors = validate_library_data(data)
        if errors:
            return jsonify({"errors":errors}), status.HTTP_BAD_REQUEST
        else:
            new_library = add_library(data)
            return jsonify(new_library.to_dict()), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/library/<int:id>', methods=['DELETE'])
def delete_library_route(id):
    try:
        deleted_library = delete_library(id)
        if deleted_library is None:
            return jsonify("library not found"), status.HTTP_NOT_FOUND
        
        return jsonify(f'library {deleted_library.id} deleted') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/library/<int:id>', methods=['PATCH'])
def update_library_route(id):
    try:
        data = {
            'name': request.form.get('name')
        }

        errors = validate_library_data(data)
        if errors:
            return jsonify({"errors": errors}), status.HTTP_BAD_REQUEST

        updated_library = update_library(id,data)
        if updated_library is None:
            return jsonify("library not found"), status.HTTP_NOT_FOUND

        return jsonify(f'library {updated_library.id} updated') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR
    

@main.route('/library/<int:id>/books')
def filter_books(id: int):
    try:
        libraries = get_libraries(id)

        if not libraries:
            return jsonify("library not found"), status.HTTP_NOT_FOUND
        
        if not libraries[0].books:
            return jsonify("No books in the library"), status.HTTP_NOT_FOUND

        return jsonify([book.to_dict() for book in libraries[0].books]), status.HTTP_OK

    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR






