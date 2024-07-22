from typing import Annotated, Any

from nestipy.common import Controller, Get, Post, Put, Delete, Request
from nestipy.common import HttpException, HttpStatus
from nestipy.ioc import Inject, Body, Param, Req
from nestipy.openapi import ApiBody, ApiConsumer

from .video_dto import CreateVideoDto, UpdateVideoDto
from .video_service import VideoService
from ..auth.auth_guards import Auth


@Auth()
@Controller('videos')
class VideoController:
    video_service: Annotated[VideoService, Inject()]

    @Get()
    async def list(self) -> list[Any]:
        return await self.video_service.list()

    @Get("/{id}")
    async def get_by_id(self, video_id: Annotated[str, Param('id')]) -> dict:
        video = await self.video_service.get(video_id)
        if not video:
            raise HttpException(HttpStatus.INTERNAL_SERVER_ERROR, "Video not found")
        return video

    @ApiBody(CreateVideoDto, ApiConsumer.MULTIPART)
    @Post()
    async def create(self, req: Annotated[Request, Req()], data: Annotated[CreateVideoDto, Body()]) -> str:
        return await self.video_service.create(data, req.user.id)

    @Put('/{id}')
    async def update(self, video_id: Annotated[str, Param('id')], data: Annotated[UpdateVideoDto, Body()]) -> str:
        return await self.video_service.update(video_id, data)

    @Delete('/{id}')
    async def delete(self, video_id: Annotated[int, Param('id')]) -> None:
        return await self.video_service.delete(video_id)
