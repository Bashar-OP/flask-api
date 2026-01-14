from flask import Blueprint, request, redirect, render_template, jsonify
from controllers.book_controller import *
import http_status as status
from routes.init import main

# import routes

@main.route('/book')
def list_books():
    title = request.args.get('title')
    author = request.args.get('author')
    books = get_books(title, author)
    return render_template('book/list_book.html', books=books)


@main.route('/book/add', methods=['GET', 'POST'])
def add_book_route():
    data = {'title':'','author':'','library_id':None}
    error = ''

    if request.method == 'GET':
        return render_template('book/add_book.html', data=data, error=error)

    data['title'] = request.form.get("title")
    data['author'] = request.form.get("author")
    data['library_id'] = request.form.get("library_id", type=int)

    error = validate_book_data(data)
    if error:
        return render_template('book/add_book.html', data=data, error=error)

    add_book(data)
    return redirect('/book')


@main.route('/book/delete/<int:id>')
def delete_book_route(id, methods=['POST']):
    delete_book(id)
    return jsonify({"message": "Book deleted"}), status.HTTP_OK


@main.route('/book/update/<int:id>', methods=['GET', 'POST'])
def update_book_route(id):

    book = get_books(id)

    if not book:
        return jsonify({"error": "Book not found"}), status.HTTP_NOT_FOUND

    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'library_id': request.form.get('library_id', type=int)
        }
        error = validate_book_data(data)
        if error:
            return jsonify({"error": error}), status.HTTP_BAD_REQUEST

        update_book(id, data)
        return redirect('/book', code=status.HTTP_SEE_OTHER)

    # GET
    return render_template('book/update_book.html', book=book), status.HTTP_OK
