from flask import Blueprint, request, redirect, render_template, jsonify
from controllers import *
import http_status as status

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')



# book

@main.route('/book')
def list_books():
    title = request.args.get('title')
    author = request.args.get('author')
    books = get_books(title, author)
    return render_template('list_book.html', books=books)


@main.route('/book/add', methods=['GET', 'POST'])
def add_book_route():
    data = {'title':'','author':'','library_id':None}
    error = ''

    if request.method == 'GET':
        return render_template('add_book.html', data=data, error=error)

    data['title'] = request.form.get("title")
    data['author'] = request.form.get("author")
    data['library_id'] = request.form.get("library_id", type=int)

    error = validate_book_data(data)
    if error:
        return render_template('add_book.html', data=data, error=error)

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
    return render_template('update_book.html', book=book), status.HTTP_OK


# Library

@main.route('/library')
def list_libraries_route():
    libraries = get_libraries()
    return render_template('list_library.html', libraries=libraries)


@main.route('/library/add', methods=['GET', 'POST'])
def add_library_route():
    if request.method == 'POST':
        name = request.form.get("name")
        add_library(name)
        return redirect('/library')
    return render_template('add_library.html')


@main.route('/library/delete/<int:id>')
def delete_library_route(id, methods=['POST']):
    delete_library(id)
    return redirect('/library')


@main.route('/library/update/<int:id>', methods=['GET', 'POST'])
def update_library_route(id):
    library = get_libraries(id)

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return render_template('update_library.html', library=library, error="Name cannot be empty")
        
        update_library(id, name)
        return redirect('/library')

    # GET
    return render_template('update_library.html', library=library)


@main.route('/library/<int:id>')
def filter_books_by_library(id):
    library = get_library_books(id)
    return render_template('filter_books.html', library=library)

# User

@main.route('/user')
def list_users_route():
    users = get_users()
    return render_template('list_user.html', users=users)


@main.route('/user/add', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        name = request.form.get("name")
        add_user(name)
        return redirect('/user')
    return render_template('add_user.html')


@main.route('/user/delete/<int:id>')
def delete_user_route(id, methods=['POST']):
    delete_user(id)
    return redirect('/user')


@main.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user_route(id):
    user = get_users(id)

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return render_template('update_user.html', user=user, error="Name cannot be empty")
        
        update_user(id, name)
        return redirect('/user')

    # GET
    return render_template('update_user.html', user=user)


# ----------

@main.route('/library/<int:id>')
def filter_books_by_library(id):
    library = get_library_books(id)
    return render_template('filter_books.html', library=library)

@main.route('/user/<int:id>/library')
def get_user_books(id):
    user = get_users(id)
    user.library
    return render_template('filter_books.html', library=library)

