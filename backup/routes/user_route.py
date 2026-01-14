from flask import request, redirect, render_template, jsonify
from controllers.user_controller import *
import http_status as status
from routes.init import main

@main.route('/user')
def list_users_route():
    users = get_users()
    return render_template('user/list_user.html', users=users)


@main.route('/user/add', methods=['GET', 'POST'])
def add_user_route():
    data = {'title':'','author':'','library_id':None}
    error = ''

    if request.method == 'POST':
        data['name'] = request.form.get("name")
        data['library_id'] = request.form.get("library_id", type=int)
        
        error = validate_user_data(data)
        if error:
            return render_template('user/add_user.html', data=data, error=error)
        add_user(data)
        return redirect('/user')
    
    return render_template('user/add_user.html',data=data, error=error)


@main.route('/user/delete/<int:id>')
def delete_user_route(id, methods=['POST']):
    delete_user(id)
    return redirect('/user')


@main.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user_route(id):
    user = get_users(id)

    if not user:
        return jsonify({"error": "User not found"}), status.HTTP_NOT_FOUND

    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'library_id': request.form.get('library_id', type=int)
        }
        error = validate_user_data(data)
        if error:
            return jsonify({"error": error}), status.HTTP_BAD_REQUEST

        update_user(id, data)
        return redirect('/user', code=status.HTTP_SEE_OTHER)

    # GET
    return render_template('user/update_user.html', user=user), status.HTTP_OK


@main.route('/user/<int:id>/library')
def get_user_books(id):
    user = get_users(id)
    library = user.library
    return render_template('library/filter_books.html', library = library)


