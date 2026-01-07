from fastapi import Depends, Cookie, HTTPException
from sqlalchemy import select

from backend.database.hash import security
from backend.database.database import session_dep
from backend.models.models import UserModel, Role


async def get_user_token(token: str = Cookie):

    try:
        payload = security._decode_token(token)
        user_id = int(payload.sub)
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail='No token')


async def check_admin(session: session_dep, admin_id: int = Depends(get_user_token)):

    query = await session.execute(select(UserModel).where(UserModel.id == admin_id))
    current_admin = query.scalar_one_or_none()

    if not current_admin:
        raise HTTPException(status_code=404, detail='Admin not found')

    if current_admin.role != Role.admin:
        raise HTTPException(status_code=403, detail='You are not an admin')

    return current_admin