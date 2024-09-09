from typing import Annotated

from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import immediateload

from .follow_dto import CreateFollowDto
from .models.follow_model import Follow


@Injectable()
class FollowService:
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def followers(self, user_id: str):
        async with self.db_service.session as session:
            stmt = (
                select(Follow).where(Follow.user_id == user_id).options(
                    immediateload(Follow.user, Follow.following)
                ).order_by(
                    desc(Follow.created_at)
                )
            )
            result = await session.execute(stmt)
            followers = result.scalars().all()
        return followers

    async def following(self, user_id: str):
        async with AsyncSession(self.db_service.engine) as session:
            stmt = (
                select(Follow).where(Follow.following_id == user_id).options(
                    immediateload(Follow.following, Follow.user)
                ).order_by(
                    desc(Follow.created_at)
                )
            )
            result = await session.execute(stmt)
            followings = result.scalars().all()
        return followings

    async def follow(self, user_id: int, data: CreateFollowDto):
        async with AsyncSession(self.db_service.engine) as session:
            follow = Follow(
                user_id=user_id,
                following_id=data.user_id
            )
            session.add(follow)
            await session.commit()
            await session.refresh(follow)
        return follow

    async def unfollow(self, user_id: int, following_id: int):
        async with AsyncSession(self.db_service.engine) as session:
            stmt = delete(Follow).where(Follow.following_id == user_id & Follow.following_id == following_id).options()
            result = await session.execute(stmt)
        return result.scalar()
