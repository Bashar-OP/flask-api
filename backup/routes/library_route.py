from flask import request, redirect, render_template, jsonify
from controllers.library_controller import *
import http_status as status
from routes.init import main

# Library

@main.route('/library')
def list_libraries_route():
    libraries = get_libraries()
    return render_template('library/list_library.html', libraries=libraries)


@main.route('/library/add', methods=['GET', 'POST'])
def add_library_route():
    if request.method == 'POST':
        name = request.form.get("name")
        add_library(name)
        return redirect('/library')
    return render_template('library/add_library.html')


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
            return render_template('library/update_library.html', library=library, error="Name cannot be empty")
        
        update_library(id, name)
        return redirect('/library')

    # GET
    return render_template('library/update_library.html', library=library)


@main.route('/library/<int:id>')
def filter_books_by_library(id):
    library = get_library_books(id)
    return render_template('library/filter_books.html', library=library)
