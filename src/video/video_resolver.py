from typing import Annotated

from nestipy.common import Request
from nestipy.graphql import Resolver, Query, Mutation
from nestipy.ioc import Inject, Arg, Req

from .models.video_model import VideoGQL, VideoRelatedModel
from .video_dto import CreateVideoDto
from .video_input import CreateVideoInput
from .video_service import VideoService
from ..auth.auth_guards import Auth


@Auth()
@Resolver()
class VideoResolver:
    video_service: Annotated[VideoService, Inject()]

    @Query()
    async def list_video(self) -> list[VideoGQL]:
        videos = await self.video_service.list()
        return [VideoGQL.from_pydantic(VideoRelatedModel.model_validate(v)) for v in videos]

    @Mutation()
    async def create_video(self, data: Annotated[CreateVideoInput, Arg()], req: Annotated[Request, Req()]) -> VideoGQL:
        video_dto = CreateVideoDto(title=data.title, description=data.description, video=data.video[0])
        video = await self.video_service.create(video_dto, req.user.id)
        return VideoGQL.from_pydantic(video)
