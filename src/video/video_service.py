import os.path
import uuid
from typing import Annotated

import anyio
from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_prisma import PrismaService
from prisma.types import VideoCreateInput, VideoInclude
from prisma.types import FindManyCommentArgsFromVideo, CommentIncludeFromLikeRecursive1
from prisma.types import FindManyLikeArgsFromVideo, LikeIncludeFromLikeRecursive1

from .video_dto import CreateVideoDto, UpdateVideoDto, CommentDto


@Injectable()
class VideoService:
    prisma: Annotated[PrismaService, Inject()]

    async def list(self):
        videos = await self.prisma.video.find_many(
            include=VideoInclude(
                user=True,
                likes=FindManyLikeArgsFromVideo(
                    include=LikeIncludeFromLikeRecursive1(
                        user=True
                    )
                ),
                comments=FindManyCommentArgsFromVideo(
                    include=CommentIncludeFromLikeRecursive1(
                        user=True
                    )
                )
            )
        )
        return [v.model_dump(mode='json') for v in videos]

    async def create(self, data: CreateVideoDto, user_id: str):
        hashed_name = f"{uuid.uuid4().hex}.{data.video.filename.split('.')[-1]}"
        file_obj = await anyio.open_file(os.path.join(os.getcwd(), "assets", "uploads", f"{hashed_name}"), "wb+")
        content = await data.video.read(-1)
        await file_obj.write(content)
        await file_obj.aclose()
        return await self.prisma.video.create(data=VideoCreateInput(
            description=data.description,
            title=data.title,
            url=hashed_name,
            userId=user_id
        ))

    async def comment(self, vide_id:str, data: CommentDto):
        pass

    async def update(self, id: int, data: UpdateVideoDto):
        return "test"

    async def delete(self, id: int):
        return "test"
