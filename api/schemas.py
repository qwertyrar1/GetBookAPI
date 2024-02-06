import uuid

from pydantic import BaseModel


class TuneModel(BaseModel):
    class Config:
        from_attributes = True


class ShowBook(TuneModel):
    book_id: uuid.UUID
    name: str
    download_link: str


class BookCreate(BaseModel):
    name: str
    download_link: str


class DeleteBookResponse(BaseModel):
    deleted_book_id: uuid.UUID