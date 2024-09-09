from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete
from nestipy.ioc import Inject, Body, Param
from nestipy.openapi import ApiBody

from src.auth.auth_guards import Auth
from .like_dto import CreateLikeDto, UpdateLikeDto
from .like_service import LikeService


@Auth()
@Controller('/like')
class LikeController:
    like_service: Annotated[LikeService, Inject()]

    @Get()
    async def likes(self) -> str:
        return await self.like_service.list()

    @ApiBody(CreateLikeDto)
    @Post()
    async def like(self, data: Annotated[CreateLikeDto, Body()]) -> str:
        return await self.like_service.create(data)

    @Delete('/{like_id}')
    async def unlike(self, like_id: Annotated[int, Param('like_id')]) -> None:
        return await self.like_service.delete(like_id)
