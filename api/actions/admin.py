from typing import Union
from uuid import UUID

from api.schemas import ShowAdmin
from api.schemas import AdminCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db.dals import AdminDAL
from hashing import Hasher


async def _create_new_admin(body: AdminCreate, session) -> ShowAdmin:
    async with session.begin():
        admin_dal = AdminDAL(session)
        admin = await admin_dal.create_admin(
            nickname=body.nickname,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowAdmin(
            admin_id=admin.id,
            nickname=admin.nickname,
        )


async def _delete_admin(admin_id, session) -> Union[UUID, None]:
    async with session.begin():
        admin_dal = AdminDAL(session)
        deleted_admin_id = await admin_dal.delete_admin(
            admin_id=admin_id,
        )
        return deleted_admin_id


async def _get_admin_by_id(admin_id, session) -> Union[ShowAdmin, None]:
    async with session.begin():
        admin_dal = AdminDAL(session)
        admin = await admin_dal.get_admin_by_id(
            admin_id=admin_id,
        )
        if admin is not None:
            return ShowAdmin(
                admin_id=admin.id,
                nickname=admin.nickname
            )


async def _get_admin_by_nickname(nickname: str, session: AsyncSession):
    async with session.begin():
        admin_dal = AdminDAL(session)
        return await admin_dal.get_admin_by_nickname(
            nickname=nickname,
        )