from typing import Annotated, Any

import bcrypt
from nestipy.common import Injectable, HttpException, HttpStatusMessages, HttpStatus
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from nestipy_jwt import JwtService
from sqlalchemy.future import select

from .auth_dto import LoginDto, RegisterDto
from ..user.models.user_model import User


@Injectable()
class AuthService:
    jwt_service: Annotated[JwtService, Inject()]
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def login(self, data: LoginDto):
        async with self.db_service.session as session:
            stmt = select(User).where(
                (User.username == data.username) | (User.email == data.username))
            result = await session.execute(stmt)
            user = result.scalars().first()
        if user is not None and bcrypt.checkpw(data.password.encode(), user.password.encode()):
            return self._generate_token(user)

        raise HttpException(
            HttpStatus.UNAUTHORIZED,
            HttpStatusMessages.UNAUTHORIZED
        )

    async def register(self, data: RegisterDto):

        try:
            async with self.db_service.session as session:
                user = User(
                    email=data.email,
                    password=bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode(),
                    username=data.username,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                if user is not None:
                    return self._generate_token(user)
        except Exception as e:
            raise HttpException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                str(e)
            )

    def _generate_token(self, user: Any):
        return {
            "token": self.jwt_service.encode({'id': user.id}, algorithm="HS256")
        }

    async def check(self, token: str) -> Any:
        _token: dict = self.jwt_service.decode(token)
        async with self.db_service.session as session:
            stmt = select(User).where(User.id == _token.get('id'))
            result = await session.execute(stmt)
            user = result.scalars().first()
            await session.close()
        if user is not None:
            return user
        else:
            return None
