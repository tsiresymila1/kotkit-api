from typing import Annotated

from nestipy.common import Controller, Get, Post, Put, Delete, Request
from nestipy.ioc import Inject, Body, Param, Req
from nestipy_alchemy import SqlAlchemyPydanticLoader, SQLAlchemyService

from src.auth.auth_guards import Auth
from .user_dto import CreateUserDto, UpdateUserDto
from .user_service import UserService


@Auth()
@Controller('users')
class UserController:
    user_service: Annotated[UserService, Inject()]
    p_sq_loader: Annotated[SqlAlchemyPydanticLoader, Inject()]
    db_service: Annotated[SQLAlchemyService, Inject()]

    @Get()
    async def list(self) -> list[dict]:
        users = await self.user_service.list()
        return [(await u.to_dict(self.db_service.session, depth=3)) for u in users]

    @Get('/me')
    async def me(self, req: Annotated[Request, Req()]) -> dict:
        return await req.user.to_dict(self.db_service.session, depth=3)

    @Post()
    async def create(self, data: Annotated[CreateUserDto, Body()]) -> str:
        return await self.user_service.create(data)

    @Put('/{id}')
    async def update(self, user_id: Annotated[int, Param('id')], data: Annotated[UpdateUserDto, Body()]) -> str:
        return await self.user_service.update(user_id, data)

    @Delete('/{id}')
    async def delete(self, user_id: Annotated[int, Param('id')]) -> None:
        return await self.user_service.delete(user_id)
