from typing import Annotated

from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from sqlalchemy.future import select
from sqlalchemy.orm import immediateload

from .comment_dto import CreateCommentDto, UpdateCommentDto
from .models.comment_model import Comment


@Injectable()
class CommentService:
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def list(self, video_id: str):
        async with self.db_service.session as session:
            stmt = select(Comment).options(
                immediateload(Comment.user),
                immediateload(Comment.video),
                immediateload(Comment.replies)
            ).where(Comment.video_id == video_id).limit(20).order_by(Comment.created_at)
            result = await session.execute(stmt)
            comments = result.scalars().all()
            await session.close()
        return comments

    async def create(self, user_id: str, data: CreateCommentDto):
        async with self.db_service.session as session:
            comment = Comment(
                text=data.comment,
                user_id=user_id,
                video_id=data.video_id,
            )
            session.add(comment)
            await session.commit()
            await session.refresh(comment)

        return comment

    async def update(self, id: int, data: UpdateCommentDto):
        return "test"

    async def delete(self, id: int):
        return "test"
