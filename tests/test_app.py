import pytest
import sys
from unittest.mock import patch, MagicMock, AsyncMock
sys.path.append("../")
from app import app

@pytest.mark.asyncio
@patch('app.async_session')
async def test_add_book(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_new_book = MagicMock()
    mock_new_book.id = 1
    mock_new_book.title = 'Test Book'
    mock_new_book.author = 'Test Author'
    mock_new_book.genre = 'Test Genre'
    mock_new_book.year_published = 2021
    mock_new_book.summary = 'Test Summary'

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    mock_session.add.side_effect = lambda book: setattr(book, 'id', 1)

    async with app.test_client() as client:
        response = await client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year_published': 2021,
            'summary': 'Test Summary'
        })

    assert response.status_code == 201
    response_json = await response.get_json()
    assert response_json == {
        'id': 1,
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Test Genre',
        'year_published': 2021,
        'summary': 'Test Summary',
    }

@pytest.mark.asyncio
@patch('app.async_session')
async def test_get_books(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_book = MagicMock()
    mock_book.id = 1
    mock_book.title = 'Test Book'
    mock_book.author = 'Test Author'
    mock_book.genre = 'Test Genre'
    mock_book.year_published = 2021
    mock_book.summary = 'Test Summary'

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.all.return_value = [mock_book]

    async with app.test_client() as client:
        response = await client.get('/books')

    assert response.status_code == 200
    response_json = await response.get_json()
    assert response_json == [{
        'id': 1,
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Test Genre',
        'year_published': 2021,
        'summary': 'Test Summary',
    }]

@pytest.mark.asyncio
@patch('app.async_session')
async def test_get_book(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_book = MagicMock()
    mock_book.id = 1
    mock_book.title = 'Test Book'
    mock_book.author = 'Test Author'
    mock_book.genre = 'Test Genre'
    mock_book.year_published = 2021
    mock_book.summary = 'Test Summary'

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = mock_book

    async with app.test_client() as client:
        response = await client.get('/books/1')

    assert response.status_code == 200
    response_json = await response.get_json()
    assert response_json == {
        'id': 1,
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Test Genre',
        'year_published': 2021,
        'summary': 'Test Summary',
    }

@pytest.mark.asyncio
@patch('app.async_session')
async def test_update_book(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_book = MagicMock()
    mock_book.id = 1
    mock_book.title = 'Old Title'
    mock_book.author = 'Old Author'
    mock_book.genre = 'Old Genre'
    mock_book.year_published = 2020
    mock_book.summary = 'Old Summary'

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = mock_book

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async with app.test_client() as client:
        response = await client.put('/books/1', json={
            'title': 'New Title',
            'author': 'New Author',
            'genre': 'New Genre',
            'year_published': 2021,
            'summary': 'New Summary'
        })

    assert response.status_code == 200
    response_json = await response.get_json()
    assert response_json == {
        'id': 1,
        'title': 'New Title',
        'author': 'New Author',
        'genre': 'New Genre',
        'year_published': 2021,
        'summary': 'New Summary',
    }


@pytest.mark.asyncio
@patch('app.async_session')
async def test_delete_book(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_book = MagicMock()
    mock_book.id = 1

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = mock_book

    # Mock session.delete() and session.commit()
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    async with app.test_client() as client:
        response = await client.delete('/books/1')

    assert response.status_code == 204


@pytest.mark.asyncio
@patch('app.async_session')
async def test_add_review(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session

    mock_book = MagicMock()
    mock_book.id = 1

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = mock_book

    mock_new_review = MagicMock()
    mock_new_review.id = 1
    mock_new_review.book_id = 1
    mock_new_review.review_text = 'Great book!'
    mock_new_review.rating = 5

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async with app.test_client() as client:
        response = await client.post('/books/1/reviews', json={
            'review_text': 'Great book!',
            'rating': 5
        })

    assert response.status_code == 201


@pytest.mark.asyncio
@patch('app.async_session')
async def test_get_reviews(mock_async_session):
    mock_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value = mock_session
    mock_review = MagicMock()
    mock_review.id = 1
    mock_review.book_id = 1
    mock_review.review_text = 'Great book!'
    mock_review.rating = 5

    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.all.return_value = [mock_review]

    async with app.test_client() as client:
        response = await client.get('/books/1/reviews')

    assert response.status_code == 200
    response_json = await response.get_json()
    assert response_json == [{
        'id': 1,
        'book_id': 1,
        'review_text': 'Great book!',
        'rating': 5,
    }]
