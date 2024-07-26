import os.path
import uuid
from typing import Annotated

import anyio
from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.orm import immediateload

from src.comment.models.comment_model import Comment
from src.like.models.like_model import Like
from .models.video_model import Video, VideoRelatedModel, VideoModel
from .video_dto import CreateVideoDto, UpdateVideoDto, CommentDto


@Injectable()
class VideoService:
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def list(self):
        async with self.db_service.session as session:
            stmt = (
                select(Video)
                .options(
                    immediateload(Video.user),
                    immediateload(Video.likes).immediateload(Like.user),
                    immediateload(Video.comments).immediateload(Comment.user)
                ).order_by(desc(Video.created_at))
            )
            result = await session.execute(stmt)
            videos = result.scalars().all()
            video_serialized = [VideoRelatedModel.model_validate(v).model_dump(mode='json') for v in videos]

        return video_serialized

    async def get(self, video_id):
        async with self.db_service.session as session:
            video = await session.get(Video, video_id)
            if video:
                return VideoModel.model_validate(video)
        return None

    async def create(self, data: CreateVideoDto, user_id: str):
        hashed_name = f"{uuid.uuid4().hex}.{data.video.filename.split('.')[-1]}"
        file_obj = await anyio.open_file(os.path.join(os.getcwd(), "assets", "uploads", f"{hashed_name}"), "wb+")
        content = await data.video.read(-1)
        await file_obj.write(content)
        await file_obj.aclose()
        async with self.db_service.session as session:
            video = Video(
                description=data.description,
                title=data.title,
                url=hashed_name,
                user_id=user_id
            )
            session.add(video)
            await session.commit()
            await session.refresh(video)

        return VideoModel.model_validate(video)

    async def comment(self, vide_id: str, data: CommentDto):
        pass

    async def update(self, id: str, data: UpdateVideoDto):
        return "test"

    async def delete(self, id: int):
        return "test"
