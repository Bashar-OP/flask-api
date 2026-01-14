from models import Book, Library, User
from extensions import db
from sqlalchemy import or_


# Book

def get_books(id=None,title=None, author=None):
    if id:
        return Book.query.get_or_404(id)
    
    if title or author:
        return db.session.execute(
            db.select(Book).where(
                or_(Book.title == title, Book.author == author)
            )
        ).scalars().all()
    return Book.query.all()


def add_book(data):
    book = Book(title=data['title'], author=data['author'], library_id=data['library_id'])
    db.session.add(book)
    db.session.commit()
    return book


def update_book(book_id, data):
    book = Book.query.get_or_404(book_id)
    if data.get('title'):
        book.title = data['title']
    if data.get('author'):
        book.author = data['author']
    if data.get('library_id'):
        book.library_id = data['library_id']
    db.session.commit()
    return book


def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()


def validate_book_data(data):
    if not data.get('title'):
        return 'title is empty'
    if not data.get('author'):
        return 'author is empty'
    if not data.get('library_id'):
        return 'library id is empty'
    if Library.query.get(data['library_id']) is None:
        return 'library id is invalid'
    return ''


# Library

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


# User


def get_users(id=None)->User|list[User]:
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


