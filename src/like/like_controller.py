from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete
from nestipy.ioc import Inject, Body, Param

from src.auth.auth_guards import Auth
from .like_dto import CreateLikeDto, UpdateLikeDto
from .like_service import LikeService


@Auth()
@Controller('videos/{video_id}/likes')
class LikeController:
    like_service: Annotated[LikeService, Inject()]

    @Get()
    async def list(self) -> str:
        return await self.like_service.list()

    @Post()
    async def create(self, data: Annotated[CreateLikeDto, Body()]) -> str:
        return await self.like_service.create(data)

    @Put('/{like_id}')
    async def update(self, like_id: Annotated[int, Param('like_id')], data: Annotated[UpdateLikeDto, Body()]) -> str:
        return await self.like_service.update(like_id, data)

    @Delete('/{like_id}')
    async def delete(self, like_id: Annotated[int, Param('like_id')]) -> None:
        return await self.like_service.delete(like_id)
