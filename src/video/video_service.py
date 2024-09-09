import os.path
import uuid
from typing import Annotated

import anyio
from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models.video_model import Video
from .video_dto import CreateVideoDto, UpdateVideoDto, CommentDto


@Injectable()
class VideoService:
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def list(self):
        async with self.db_service.session as session:
            stmt = (
                select(Video).order_by(desc(Video.created_at))
            )
            result = await session.execute(stmt)
            videos = result.scalars().all()
        return videos

    async def get(self, video_id):
        async with self.db_service.session as session:
            video = await session.get(Video, video_id)
        return video

    async def create(self, data: CreateVideoDto, user_id: str):
        ext = data.video.filename.split('.')[-1]
        hashed_name = f"{uuid.uuid4().hex}.{ext if ext != 'temp' else 'mp4'}"
        file_obj = await anyio.open_file(os.path.join(os.getcwd(), "assets", "uploads", f"{hashed_name}"), "wb+")
        content = await data.video.read(-1)
        await file_obj.write(content)
        await file_obj.aclose()
        async with AsyncSession(self.db_service.engine) as session:
            video = Video(
                description=data.description,
                title=data.title,
                url=hashed_name,
                user_id=user_id
            )
            session.add(video)
            await session.commit()
            await session.refresh(video)
        return video

    async def comment(self, vide_id: str, data: CommentDto):
        pass

    async def update(self, id: str, data: UpdateVideoDto):
        return "test"

    async def delete(self, id: int):
        return "test"
