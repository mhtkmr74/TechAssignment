from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    year_published = db.Column(db.Integer)
    summary = db.Column(db.Text)

    reviews = db.relationship('Review', backref='book', lazy=True, cascade="all, delete-orphan")


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Review {self.id} - Book {self.book_id} - Rating {self.rating}>'
