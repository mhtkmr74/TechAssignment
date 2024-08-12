import asyncio
from quart import Quart, jsonify, request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Book, Review, Base
from swagger_ui import quart_api_doc
from config import DATABASE_URL
from authenticate import requires_auth

app = Quart(__name__)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

quart_api_doc(app, config_path='./static/openapi.yaml', url_prefix='/api/doc', title='API doc')


@app.before_serving
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.route('/books', methods=['POST'])
@requires_auth
async def add_book():
    data = await request.get_json()
    async with async_session() as session:
        async with session.begin():
            new_book = Book(
                title=data['title'],
                author=data['author'],
                genre=data['genre'],
                year_published=data['year_published'],
                summary=data['summary']
            )
            session.add(new_book)
        await session.commit()
        return jsonify({
            'id': new_book.id,
            'title': new_book.title,
            'author': new_book.author,
            'genre': new_book.genre,
            'year_published': new_book.year_published,
            'summary': new_book.summary,
        }), 201


@app.route('/books', methods=['GET'])
@requires_auth
async def get_books():
    async with async_session() as session:
        result = await session.execute(select(Book))
        books = result.scalars().all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year_published': book.year_published,
            'summary': book.summary,
        } for book in books])


@app.route('/books/<int:id>', methods=['GET'])
@requires_auth
async def get_book(id):
    async with async_session() as session:
        result = await session.execute(select(Book).filter(Book.id == id))
        book = result.scalars().first()
        if book:
            return jsonify({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'year_published': book.year_published,
                'summary': book.summary,
            })
        else:
            return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<int:id>', methods=['PUT'])
@requires_auth
async def update_book(id):
    data = await request.get_json()
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Book).filter(Book.id == id))
            book = result.scalars().first()
            if not book:
                return jsonify({'error': 'Book not found'}), 404

            for key, value in data.items():
                setattr(book, key, value)

            session.add(book)
        await session.commit()
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year_published': book.year_published,
            'summary': book.summary,
        })

@app.route('/books/<int:id>', methods=['DELETE'])
@requires_auth
async def delete_book(id):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Book).filter(Book.id == id))
            book = result.scalars().first()
            if not book:
                return jsonify({'error': 'Book not found'}), 404

            await session.delete(book)
        await session.commit()
        return '', 204

@app.route('/books/<int:id>/reviews', methods=['POST'])
@requires_auth
async def add_review(id):
    data = await request.get_json()
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Book).filter(Book.id == id))
            book = result.scalars().first()
            if not book:
                return jsonify({'error': 'Book not found'}), 404

            new_review = Review(
                book_id=id,
                user_id=1,
                review_text=data['review_text'],
                rating=data['rating']
            )
            session.add(new_review)
        await session.commit()
        return jsonify({
            'id': new_review.id,
            'book_id': new_review.book_id,
            'review_text': new_review.review_text,
            'rating': new_review.rating,
        }), 201

@app.route('/books/<int:id>/reviews', methods=['GET'])
@requires_auth
async def get_reviews(id):
    async with async_session() as session:
        result = await session.execute(select(Review).filter(Review.book_id == id))
        reviews = result.scalars().all()
        return jsonify([{
            'id': review.id,
            'book_id': review.book_id,
            'review_text': review.review_text,
            'rating': review.rating,
        } for review in reviews])


if __name__ == '__main__':
    app.run(debug=True)