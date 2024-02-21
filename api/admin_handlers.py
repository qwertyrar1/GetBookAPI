from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.admin import _create_new_admin, _delete_admin, _get_admin_by_id
from api.actions.auth import get_current_admin_from_token
from api.schemas import DeleteModelResponse
from api.schemas import ShowAdmin
from api.schemas import AdminCreate
from db.models import Admin
from db.session import get_db

logger = getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ShowAdmin)
async def create_admin(
        body: AdminCreate,
        db: AsyncSession = Depends(get_db),
        current_admin: Admin = Depends(get_current_admin_from_token)) -> ShowAdmin:
    try:
        if not current_admin.is_superadmin:
            raise HTTPException(status_code=403, detail="Forbidden.")
        return await _create_new_admin(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.delete("/", response_model=DeleteModelResponse)
async def delete_admin(
    admin_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_from_token),
) -> DeleteModelResponse:
    if not current_admin.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_admin_id = await _delete_admin(admin_id, db)
    if deleted_admin_id is None:
        raise HTTPException(
            status_code=404, detail=f"Admin with id {admin_id} not found."
        )
    return DeleteModelResponse(deleted_id=deleted_admin_id)


@router.get("/", response_model=ShowAdmin)
async def get_admin_by_id(
    admin_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_from_token),
) -> ShowAdmin:
    if not current_admin.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    admin = await _get_admin_by_id(admin_id, db)
    if admin is None:
        raise HTTPException(
            status_code=404, detail=f"Admin with id {admin_id} not found."
        )
    return admin



