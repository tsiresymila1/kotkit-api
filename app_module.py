from src.follow.follow_module import FollowModule
from typing import Annotated

from nestipy.common import Module, ModuleProviderDict, UploadFile
from nestipy.graphql import GraphqlModule, GraphqlOption
from nestipy.ioc import Inject
from nestipy_alchemy import (SQLAlchemyModule, SQLAlchemyOption,
                             SqlAlchemyPydanticLoader, SQLAlchemyService)
from nestipy_config import ConfigModule, ConfigService
from nestipy_jwt import JwtModule, JwtOption
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.file_uploads import Upload
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader

from base_model import Base, p_sq_mapper, s_sq_mapper
from src.auth.auth_module import AuthModule
from src.comment.comment_module import CommentModule
from src.like.like_module import LikeModule
from src.user.user_module import UserModule
from src.video.video_module import VideoModule

s_sq_mapper.finalize()


def sqlalchemy_factory(config: Annotated[ConfigService, Inject()]) -> SQLAlchemyOption:
    return SQLAlchemyOption(
        url=config.get("DATABASE_URL"),
        sync=False,
        declarative_base=Base
    )


def sqlalchemy_to_pydantic_factory(service: Annotated[SQLAlchemyService, Inject()]) -> SqlAlchemyPydanticLoader:
    return SqlAlchemyPydanticLoader(
        _mapper=p_sq_mapper,
        async_bind_factory=lambda: AsyncSession(
            service.engine,
            expire_on_commit=False
        )
    )


def update_context(service: Annotated[SQLAlchemyService, Inject()]):
    return {
        "sqlalchemy_loader": StrawberrySQLAlchemyLoader(
            async_bind_factory=lambda: AsyncSession(
                service.engine,
                expire_on_commit=False
            )
        )
    }


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
        GraphqlModule.for_root(options=GraphqlOption(
            schema_option={
                "scalar_overrides": {UploadFile: Upload},
                "types": s_sq_mapper.mapped_types.values()
            },
            context_callback=update_context
        )),
        AuthModule,
        UserModule,
        VideoModule,
        CommentModule,
        LikeModule,
        FollowModule
    ],
    providers=[
        ModuleProviderDict(
            token=SqlAlchemyPydanticLoader,
            factory=sqlalchemy_to_pydantic_factory,
            inject=[SQLAlchemyService],
            imports=[SQLAlchemyModule]
        )
    ]
)
class AppModule:
    ...
