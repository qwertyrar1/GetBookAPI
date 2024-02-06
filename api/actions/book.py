from fastapi import HTTPException
from typing import Union
from uuid import UUID

from api.schemas import ShowBook
from api.schemas import BookCreate
from db.dals import BookDAL
from db.models import Book


async def _create_new_book(body: BookCreate, session) -> ShowBook:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.create_book(
            name=body.name,
            download_link=body.download_link,
        )
        return ShowBook(
            book_id=book.id,
            name=book.name,
            download_link=book.download_link,
        )


async def _delete_book(book_id, session) -> Union[UUID, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        deleted_book_id = await book_dal.delete_book(
            book_id=book_id,
        )
        return deleted_book_id


async def _get_book_by_id(book_id, session) -> Union[Book, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.get_book_by_id(
            book_id=book_id,
        )
        if book is not None:
            return book