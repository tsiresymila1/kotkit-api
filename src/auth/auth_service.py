from typing import Annotated, Any

import bcrypt
from nestipy.common import Injectable, HttpException, HttpStatusMessages, HttpStatus
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from nestipy_jwt import JwtService
from sqlalchemy import func
from sqlalchemy.dialects import mysql
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

from .auth_dto import LoginDto, RegisterDto
from ..user.models.user_model import User

Video = aliased(User.videos.property.mapper.class_)
Follower = aliased(User.followers.property.mapper.class_)
Following = aliased(User.following.property.mapper.class_)

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
            try:
                # subquery_video = (
                #     select(func.count())
                #     .select_from(Video)
                #     .where(Video.user_id == User.id)  # Ensure you have the correct foreign key relationship
                #     .scalar_subquery()
                # )
                # subquery_follower = (
                #     select(func.count())
                #     .select_from(Follower)
                #     .where(Follower.user_id == User.id)  # Ensure you have the correct foreign key relationship
                #     .scalar_subquery()
                # )
                # subquery_followings = (
                #     select(func.count())
                #     .select_from(Following)
                #     .where(Following.following_id == User.id)  # Ensure you have the correct foreign key relationship
                #     .scalar_subquery()
                # )
                stmt = select(
                    User,
                    # subquery_video.label('video_count'),
                    # subquery_follower.label('follower_count'),
                    # subquery_followings.label('following_count')
                ).where(
                    User.id == _token.get('id')
                )
                result = await session.execute(stmt)
                user = result.scalars().first()
                # user = result.fetchone().
                await session.close()
                return user
            except Exception as e:
                print(e)
                return None

