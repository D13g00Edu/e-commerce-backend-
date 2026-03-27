from typing import Annotated

from fastapi import Depends
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ── Database ───────────────────────────────────────────────────────────────


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


DBSession = Annotated[AsyncSession, Depends(get_db)]


# ── Auth ───────────────────────────────────────────────────────────────────


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSession,
) -> User:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedException()
        user_id: str = payload.get("sub")
    except JWTError:
        raise UnauthorizedException()

    from app.repositories.user import UserRepository
    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))
    if not user:
        raise UnauthorizedException()
    if not user.is_active:
        raise UnauthorizedException("Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException()
    return current_user


CurrentAdmin = Annotated[User, Depends(get_current_admin)]
