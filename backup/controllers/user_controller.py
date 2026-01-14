from models import User,Library
from extensions import db


def get_users(id:int | None = None)->User|list[User]:
    if id:
        return User.query.get_or_404(id)
    return User.query.all()


def add_user(data):
    user = User(name=data['name'], library_id = data['library_id'])
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user_id, data):

    user = User.query.get_or_404(user_id)

    if data['name']:
        user.name = data['name']

    if data['library_id']:
        user.library_id = data['library_id']

    db.session.commit()
    return user


def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

def validate_user_data(data):
    if not data['name']:
        return 'name is empty'
    if not data['library_id']:
        return 'library id is empty'
    if Library.query.get(data['library_id']) is None:
        return 'library id is invalid'
    return ''
