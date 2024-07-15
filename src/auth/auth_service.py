from typing import Annotated, Any

import bcrypt
from nestipy.common import Injectable, HttpException, HttpStatusMessages, HttpStatus
from nestipy.ioc import Inject
from nestipy_jwt import JwtService
from nestipy_prisma import PrismaService
from prisma.types import UserWhereInput, UserCreateInput, UserWhereInputRecursive1

from .auth_dto import LoginDto, RegisterDto


@Injectable()
class AuthService:
    jwt_service: Annotated[JwtService, Inject()]
    prisma: Annotated[PrismaService, Inject()]

    async def login(self, data: LoginDto):
        user = await self.prisma.user.find_first(where=UserWhereInput(
            OR=[
                UserWhereInputRecursive1(username=data.username),
                UserWhereInputRecursive1(email=data.username)
            ]
        ))
        if user is not None and bcrypt.checkpw(data.password.encode(), user.password.encode()):
            return self.jwt_service.encode({'id': user.id}, algorithm="HS256")

        raise HttpException(
            HttpStatus.UNAUTHORIZED,
            HttpStatusMessages.UNAUTHORIZED
        )

    async def register(self, data: RegisterDto):
        try:
            user = await self.prisma.user.create(data=UserCreateInput(
                email=data.email,
                password=bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode(),
                username=data.username,
            ))
            if user is not None:
                return self.jwt_service.encode({'id': user.id}, algorithm="HS256")
        except Exception as e:
            raise HttpException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                str(e)
            )

    async def check(self, token: str) -> Any:
        decoded: dict = self.jwt_service.decode(token)
        user = await self.prisma.user.find_first(where=UserWhereInput(
            id=decoded.get('id')
        ))
        if user is not None:
            return user
        else:
            return None
