from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.book import (
    BookCreate,
    BookCreateResponse,
    BookDetailResponse,
    BookListResponse,
)


router = APIRouter()

# Temporary in-memory storage
books = []


@router.post(
    "/books",
    response_model=BookCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Create a new book by providing its title, author, and category."
)
async def create_book(book: BookCreate):

    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "category": book.category
    }

    books.append(new_book)

    return {
        "message": "Book created successfully",
        "book": new_book
    }


@router.get(
    "/books",
    response_model=BookListResponse,
    summary="Get all books",
    description="Retrieve a list of all books stored in the system."
)
async def get_books():

    return {
        "message": "Books retrieved successfully",
        "total": len(books),
        "books": books
    }


@router.get(
    "/books/{book_id}",
    response_model=BookDetailResponse,
    summary="Get a book by ID",
    description="Retrieve details of a specific book using its unique ID."
)
async def get_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return {
                "message": "Book retrieved successfully",
                "book": book
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )