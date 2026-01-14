from models import Book,Library
from extensions import db
from sqlalchemy import or_

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

