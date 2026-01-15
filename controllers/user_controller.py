from models import User,Library
from extensions import db


def get_users(id:int | None = None)-> list[User]:
    if id is None:
        return User.query.all()
    user = db.session.get(User, id)
    return [user] if user else []


def add_user(data)->User:
    user = User(name=data['name'], library_id = data['library_id'])
    db.session.add(user)
    db.session.commit()
    return user


def update_user(id:int, data:dict)->User|None:

    user = User.query.get(id)
    
    if user is None:
        return None

    if data['name'] is not None:
        user.name = data['name']

    if data['library_id'] is not None:
        user.library_id = data['library_id']

    db.session.commit()
    return user


def delete_user(id:int)-> User|None:
    user = User.query.get(id)
    if user is None:
        return None
    db.session.delete(user)
    db.session.commit()
    return user


def validate_user_data(data,mode='add'):
    errors = []
    
    if mode != 'update':
        if not data['name']:
            errors.append( 'name is empty')

    if data['library_id'] is not None:
        user = User.query.filter_by(library_id=data['library_id']).first()
        if user is not None:
            errors.append( 'another user has same library id')
        if Library.query.get(data['library_id']) is None:
            errors.append( 'library id is invalid')

    

    return errors
