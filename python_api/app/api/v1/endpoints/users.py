from typing import List

from fastapi import APIRouter, Query

from app.core.dependencies import CurrentAdmin, CurrentUser, DBSession
from app.core.exceptions import NotFoundException
from app.core.security import hash_password
from app.repositories.user import UserRepository
from app.schemas.user import UserAdminUpdate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    """Get current user profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(data: UserUpdate, current_user: CurrentUser, db: DBSession):
    """Update current user profile."""
    repo = UserRepository(db)
    return await repo.update(current_user, data.model_dump(exclude_none=True))


# ── Admin routes ───────────────────────────────────────────────────────────


@router.get("", response_model=List[UserResponse])
async def list_users(
    db: DBSession,
    _: CurrentAdmin,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """List all users (admin only)."""
    repo = UserRepository(db)
    return await repo.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DBSession, _: CurrentAdmin):
    """Get a user by ID (admin only)."""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserAdminUpdate, db: DBSession, _: CurrentAdmin):
    """Update any user (admin only)."""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise NotFoundException("User not found")
    return await repo.update(user, data.model_dump(exclude_none=True))
