from sqlalchemy import or_
from models import Book,Library
from extensions import db


def get_books(id:int | None = None,
              title:str | None = None,
              author:str | None = None)-> list[Book]:
    
    if id is None or title is None or author is None:
        return Book.query.all()
    if title is not None or author is not None:
        query = Book.query.filter(
    or_(
        Book.title == title,
        Book.author == author
    ))
        return query.all()

    book = db.session.get(Book, id)
    return [book] if book else []


def add_book(data)->Book:
    book = Book(title=data['title'],author=data['author'], library_id = data['library_id'])
    db.session.add(book)
    db.session.commit()
    return book


def update_book(id:int, data:dict)->Book|None:

    book = Book.query.get(id)
    
    if book is None:
        return None

    if data['title'] is not None:
        book.title = data['title']

    if data['author'] is not None:
        book.author = data['author']

    if data['library_id'] is not None:
        book.library_id = data['library_id']

    db.session.commit()
    return book


def delete_book(id:int)-> Book|None:
    book = Book.query.get(id)
    if book is None:
        return None
    db.session.delete(book)
    db.session.commit()
    return book


def validate_book_data(data,mode='add'):
    errors = []

    if mode != 'update':
        if data['title'] is None:
            errors.append( 'title is empty')
        if data['author'] is None:
            errors.append( 'author is empty')

    if data['library_id'] is not None:
        book = Book.query.filter_by(library_id=data['library_id']).first()
        if book is not None:
            errors.append( 'another book has same library id')
        if Library.query.get(data['library_id']) is None:
            errors.append( 'library id is invalid')

    return errors
