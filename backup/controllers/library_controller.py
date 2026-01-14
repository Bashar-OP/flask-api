from models import Library
from extensions import db

def get_libraries(id=None):
    if id:
        return Library.query.get_or_404(id)
    return Library.query.all()


def add_library(name):
    if not name:
        return None
    library = Library(name=name)
    db.session.add(library)
    db.session.commit()
    return library


def update_library(library_id, name):
    library = Library.query.get_or_404(library_id)
    if name:
        library.name = name
        db.session.commit()
    return library


def delete_library(library_id):
    library = Library.query.get_or_404(library_id)
    db.session.delete(library)
    db.session.commit()


def get_library_books(library_id):
    library = Library.query.get_or_404(library_id)
    return library

