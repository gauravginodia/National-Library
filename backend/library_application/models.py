from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_logged=db.Column(db.DateTime)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user = db.relationship('User', backref=db.backref('roles'))
    role = db.relationship('Role', backref=db.backref('users'))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    # Add a relationship to represent one-to-many with Book
    books = db.relationship('Book', backref='section', cascade="all, delete")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    authors = db.Column(db.String(100))
    isbn=db.Column(db.String(100))
    rating = db.Column(db.Float)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

class BookStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_allocated = db.Column(db.Integer)
    is_requested = db.Column(db.Integer)
    date_of_issue = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    book = db.relationship('Book', backref=db.backref('allocations'))
    user = db.relationship('User', backref=db.backref('allocations'))

class BookIssued(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating=db.Column(db.Integer)
    feedback = db.Column(db.Text)
    returned = db.Column(db.Integer)
    date_of_issue = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    user = db.relationship('User', backref=db.backref('books'))
    book = db.relationship('Book', backref=db.backref('users'))




