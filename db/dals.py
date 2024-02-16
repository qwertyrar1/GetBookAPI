from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PortalRole
from db.models import Admin
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


class AdminDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_admin(
        self,
        nickname: str,
        hashed_password: str,
    ) -> Admin:
        new_admin = Admin(
            nickname=nickname,
            hashed_password=hashed_password,
        )
        self.db_session.add(new_admin)
        await self.db_session.flush()
        return new_admin

    async def delete_admin(self, admin_id: UUID) -> Union[UUID, None]:
        query = (
            delete(Admin)
            .where(Admin.id == admin_id)
            .returning(Admin.id)
        )
        res = await self.db_session.execute(query)
        deleted_admin_id_row = res.fetchone()
        if deleted_admin_id_row is not None:
            return deleted_admin_id_row[0]

    async def get_admin_by_id(self, admin_id: UUID) -> Union[Admin, None]:
        query = select(Admin).where(Admin.id == admin_id)
        res = await self.db_session.execute(query)
        admin_row = res.fetchone()
        if admin_row is not None:
            return admin_row[0]

    async def get_admin_by_nickname(self, nickname: str) -> Union[Admin, None]:
        query = select(Admin).where(Admin.nickname == nickname)
        res = await self.db_session.execute(query)
        admin_row = res.fetchone()
        if admin_row is not None:
            return admin_row[0]
