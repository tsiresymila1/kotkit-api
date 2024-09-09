from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete, Request
from nestipy.ioc import Inject, Body, Param, Req
from nestipy.openapi import ApiBody

from .follow_dto import CreateFollowDto
from .follow_service import FollowService
from ..auth.auth_guards import Auth


@Auth()
@Controller('follow')
class FollowController:
    follow_service: Annotated[FollowService, Inject()]

    @Get('/followers')
    async def followers(self, req: Annotated[Request, Req()]) -> str:
        return await self.follow_service.followers(req.user.id)

    @Get('/following')
    async def followings(self, req: Annotated[Request, Req()]) -> str:
        return await self.follow_service.following(req.user.id)

    @ApiBody(CreateFollowDto)
    @Post()
    async def follow(self, req: Annotated[Request, Req()] ,data: Annotated[CreateFollowDto, Body()]) -> str:
        return await self.follow_service.follow(req.user.id, data)

    @Delete('/{user_id}')
    async def un_follow(self, req: Annotated[Request, Req()], follow_id: Annotated[int, Param('user_id')]) -> None:
        return await self.follow_service.unfollow(req.user.id, follow_id)
