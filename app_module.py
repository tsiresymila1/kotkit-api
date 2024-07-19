from typing import Annotated

from nestipy.common import Module
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyModule, SQLAlchemyOption
from nestipy_config import ConfigModule, ConfigService
from nestipy_jwt import JwtModule, JwtOption

from base_model import Base
from src.auth.auth_module import AuthModule
from src.comment.comment_module import CommentModule
from src.like.like_module import LikeModule
from src.user.user_module import UserModule
from src.video.video_module import VideoModule


def sqlalchemy_factory(config: Annotated[ConfigService, Inject()]) -> SQLAlchemyOption:
    return SQLAlchemyOption(
        url=config.get("DATABASE_URL"),
        sync=False,
        declarative_base=Base
    )


@Module(
    imports=[
        ConfigModule.for_root(),
        SQLAlchemyModule.for_root_async(
            factory=sqlalchemy_factory,
            inject=[ConfigService],
            imports=[ConfigModule],
            is_global=True
        ),
        JwtModule.for_root(
            option=JwtOption(
                secret="test_secret",
                is_global=True
            )
        ),
        AuthModule,
        UserModule,
        VideoModule,
        CommentModule,
        LikeModule
    ],
)
class AppModule:
    ...
