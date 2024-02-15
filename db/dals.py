from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PortalRole
from db.models import User
from db.models import Book


class BookDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_book(
        self,
        name: str,
        download_link: str,
    ) -> Book:
        new_book = Book(
            name=name,
            download_link=download_link,
        )
        self.db_session.add(new_book)
        await self.db_session.flush()
        return new_book

    async def delete_book(self, book_id: UUID) -> Union[UUID, None]:
        query = delete(Book).where(Book.id == book_id).returning(Book.id)
        res = await self.db_session.execute(query)
        deleted_book_id_row = res.fetchone()
        if deleted_book_id_row is not None:
            return deleted_book_id_row[0]

    async def get_book_by_id(self, book_id: UUID) -> Union[Book, None]:
        query = select(Book).where(Book.id == book_id)
        res = await self.db_session.execute(query)
        book_row = res.fetchone()
        if book_row is not None:
            return book_row[0]


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        nickname: str,
        hashed_password: str,
        roles: list[PortalRole],
    ) -> User:
        new_user = User(
            nickname=nickname,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            delete(User)
            .where(User.id == user_id)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
