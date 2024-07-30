from typing import Annotated

from nestipy.common import Request
from nestipy.graphql import Resolver, Query, Mutation
from nestipy.ioc import Inject, Arg, Req

from base_model import s_sq_mapper
from .video_dto import CreateVideoDto
from .video_input import CreateVideoInput
from .video_service import VideoService
from ..auth.auth_guards import Auth

Video = s_sq_mapper.mapped_types.get("Video")


@Auth()
@Resolver()
class VideoResolver:
    video_service: Annotated[VideoService, Inject()]

    @Query()
    async def list_video(self) -> list[Video]:
        return await self.video_service.list()

    @Mutation()
    async def create_video(self, data: Annotated[CreateVideoInput, Arg()], req: Annotated[Request, Req()]) -> Video:
        video_dto = CreateVideoDto(title=data.title, description=data.description, video=data.video)
        video = await self.video_service.create(video_dto, req.user.id)
        return video
