from extensions import db
from datetime import datetime

class Library(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), nullable=False)

        books = db.relationship('Book', back_populates='library')

        user = db.relationship('User', back_populates='library')

        def to_dict(self):
                return {
                "id": self.id,
                "name": self.name
                }

class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(20), nullable=False)
        author = db.Column(db.String(20), nullable=False)
        library_id = db.Column(db.Integer, db.ForeignKey('library.id'))
        library = db.relationship('Library', back_populates='books')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def to_dict(self):
                return {
                "id": self.id,
                "title": self.title,
                "author": self.author,
                "library_id": self.library_id,
                "created_at": self.created_at
                }
        
class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), nullable=False)

        library_id = db.Column(db.Integer, db.ForeignKey('library.id'),unique=True)
        library = db.relationship('Library', back_populates='user')

        def to_dict(self):
                return {
                "id": self.id,
                "name": self.name,
                "library_id": self.library_id,
                }


