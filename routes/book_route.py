from flask import  request, jsonify
from controllers.book_controller import *
import http_status as status
from routes.init import main



@main.route('/book')
def list_books():
    try:
        title = request.args.get("title")
        author = request.args.get("author")

        books = get_books(title=title,author=author)

        if not books:
            return jsonify("No books found"), status.HTTP_NOT_FOUND

        return jsonify([u.to_dict() for u in books]), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR

@main.route('/book/<int:id>')
def get_book(id: int):
    try:
        books = get_books(id)

        if not books:
            return jsonify("Book not found"), status.HTTP_NOT_FOUND

        return jsonify(books[0].to_dict()), status.HTTP_OK

    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/book', methods=['POST'])
def add_book_route():
    try:
        data = {'title':request.form.get("title"),
                'author':request.form.get("author"),
                'library_id':request.form.get("library_id", type=int)
        }

        errors = []

        errors = validate_book_data(data)
        if errors:
            return jsonify({"errors":errors}), status.HTTP_BAD_REQUEST
        else:
            new_book = add_book(data)
            return jsonify(new_book.to_dict()), status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/book/<int:id>', methods=['DELETE'])
def delete_book_route(id):
    try:
        deleted_book = delete_book(id)
        if deleted_book is None:
            return jsonify("Book not found"), status.HTTP_NOT_FOUND
        
        return jsonify(f'book {deleted_book.id} deleted') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR


@main.route('/book/<int:id>', methods=['PATCH'])
def update_book_route(id):
    try:
        data = {'title':request.form.get("title"),
                'author':request.form.get("author"),
                'library_id':request.form.get("library_id", type=int)
        }

        errors = validate_book_data(data,mode='update')
        if errors:
            return jsonify({"errors": errors}), status.HTTP_BAD_REQUEST

        updated_book = update_book(id,data)
        if updated_book is None:
            return jsonify("Book not found"), status.HTTP_NOT_FOUND

        return jsonify(f'library {updated_book.id} updated') , status.HTTP_OK
    except Exception as e:
        return jsonify(f"Something went wrong \n {e}"), status.HTTP_INTERNAL_SERVER_ERROR
    


