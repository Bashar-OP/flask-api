from models import Library
from extensions import db


def get_libraries(id:int | None = None)-> list[Library]:
    if id is None:
        return Library.query.all()
    library = db.session.get(Library, id)
    return [library] if library else []


def add_library(data)->Library:
    library = Library(name=data['name'])
    db.session.add(library)
    db.session.commit()
    return library


def update_library(id:int, data:dict)->Library|None:

    library = Library.query.get(id)

    if library is None:
        return None

    if data['name'] is not None:
        library.name = data['name']

    db.session.commit()
    return library


def delete_library(id:int)-> Library|None:
    library = Library.query.get(id)
    if library is None:
        return None
    db.session.delete(library)
    db.session.commit()
    return library


def validate_library_data(data):
    errors = []

    if not data['name']:
        errors.append( 'name is empty')
        
    return errors
