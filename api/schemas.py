import uuid

from pydantic import BaseModel


class TuneModel(BaseModel):
    class Config:
        from_attributes = True


class ShowBook(TuneModel):
    book_id: uuid.UUID
    name: str
    download_link: str


class ShowAdmin(TuneModel):
    admin_id: uuid.UUID
    nickname: str


class BookCreate(BaseModel):
    name: str
    download_link: str


class AdminCreate(BaseModel):
    nickname: str
    password: str


class DeleteModelResponse(BaseModel):
    deleted_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    token_type: str