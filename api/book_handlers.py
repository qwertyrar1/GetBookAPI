from logging import getLogger
from uuid import UUID

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.book import _delete_book, _get_book_by_id, _create_new_book
from api.actions.auth import get_current_admin_from_token
from api.schemas import ShowBook, BookCreate, DeleteModelResponse

from db.models import Book, Admin
from db.session import get_db

logger = getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ShowBook)
async def create_book(body: BookCreate, db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_from_token),) -> ShowBook:
    try:
        return await _create_new_book(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.delete("/", response_model=DeleteModelResponse)
async def delete_book(
    book_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_from_token),
) -> DeleteModelResponse:
    book_for_deletion = await _get_book_by_id(book_id, db)
    if book_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} not found."
        )
    deleted_book_id = await _delete_book(book_id, db)
    if deleted_book_id is None:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} not found."
        )
    return DeleteModelResponse(deleted_book_id=deleted_book_id)


@router.get("/", response_model=ShowBook)
async def get_book_by_id(
    book_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ShowBook:
    book = await _get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} not found."
        )
    return ShowBook(
            book_id=book.id,
            name=book.name,
            download_link=book.download_link,
        )


