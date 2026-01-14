from extensions import db
from datetime import datetime

class Library(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), nullable=False)

        books = db.relationship('Book', back_populates='library')

        user = db.relationship('User', back_populates='library')


class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(20), nullable=False)
        author = db.Column(db.String(20), nullable=False)
        library_id = db.Column(db.Integer, db.ForeignKey('library.id'))
        library = db.relationship('Library', back_populates='books')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), nullable=False)

        library_id = db.Column(db.Integer, db.ForeignKey('library.id'),unique=True)
        library = db.relationship('Library', back_populates='user')


