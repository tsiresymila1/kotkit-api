from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete
from nestipy.ioc import Inject, Body, Param, Req
from nestipy.openapi import ApiBody
from nestipy.common import Request
from src.auth.auth_guards import Auth
from .comment_dto import CreateCommentDto, UpdateCommentDto
from .comment_service import CommentService


@Auth()
@Controller('videos/{video_id}/comments')
class CommentController:
    comment_service: Annotated[CommentService, Inject()]

    @Get()
    async def list(self, video_id: Annotated[str, Param('video_id')]) -> str:
        return await self.comment_service.list(video_id)

    @ApiBody(CreateCommentDto)
    @Post()
    async def create(self, req: Annotated[Request, Req()], data: Annotated[CreateCommentDto, Body()]) -> str:
        return await self.comment_service.create(req.user.id, data)

    @Put('/{comment_id}')
    async def update(self, comment_id: Annotated[int, Param('comment_id')],
                     data: Annotated[UpdateCommentDto, Body()]) -> str:
        return await self.comment_service.update(comment_id, data)

    @Delete('/{comment_id}')
    async def delete(self, comment_id: Annotated[int, Param('comment_id')]) -> None:
        return await self.comment_service.delete(comment_id)
