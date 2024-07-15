from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete
from nestipy.ioc import Inject, Body, Param

from src.auth.auth_guards import Auth
from .user_dto import CreateUserDto, UpdateUserDto
from .user_service import UserService


@Auth()
@Controller('users')
class UserController:
    user_service: Annotated[UserService, Inject()]

    @Get()
    async def list(self) -> str:
        return await self.user_service.list()

    @Post()
    async def create(self, data: Annotated[CreateUserDto, Body()]) -> str:
        return await self.user_service.create(data)

    @Put('/{id}')
    async def update(self, user_id: Annotated[int, Param('id')], data: Annotated[UpdateUserDto, Body()]) -> str:
        return await self.user_service.update(user_id, data)

    @Delete('/{id}')
    async def delete(self, user_id: Annotated[int, Param('id')]) -> None:
        return await self.user_service.delete(user_id)
