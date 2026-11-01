from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str


class BookCreateResponse(BaseModel):
    message: str
    book: BookResponse


class BookDetailResponse(BaseModel):
    message: str
    book: BookResponse


class BookListResponse(BaseModel):
    message: str
    total: int
    books: list[BookResponse]