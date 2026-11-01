from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.api.books import books


client = TestClient(app)


def setup_function():
    """Reset book storage before every test."""
    books.clear()


def test_create_book():

    response = client.post(
        "/api/v1/books",
        json={
            "title": "Deep Learning",
            "author": "Ian Goodfellow",
            "category": "Artificial Intelligence"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["book"]["title"] == "Deep Learning"
    assert data["book"]["author"] == "Ian Goodfellow"


def test_get_all_books():

    client.post(
        "/api/v1/books",
        json={
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "category": "Programming"
        }
    )

    response = client.get("/api/v1/books")

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_get_existing_book():

    client.post(
        "/api/v1/books",
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "category": "Software Engineering"
        }
    )

    response = client.get("/api/v1/books/1")

    assert response.status_code == 200
    assert response.json()["book"]["title"] == "Clean Code"


def test_get_non_existing_book():

    response = client.get("/api/v1/books/999")

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Book with ID 999 not found"
    )


def test_create_book_with_invalid_data():

    response = client.post(
        "/api/v1/books",
        json={
            "title": "",
            "author": "Ian Goodfellow",
            "category": "AI"
        }
    )

    assert response.status_code == 422