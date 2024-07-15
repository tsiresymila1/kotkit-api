from nestipy.common import Module
from nestipy_jwt import JwtModule, JwtOption
from nestipy_prisma import PrismaModule

from src.auth.auth_module import AuthModule
from src.user.user_module import UserModule
from src.video.video_module import VideoModule


@Module(
    imports=[
        PrismaModule.for_root(),
        JwtModule.for_root(
            option=JwtOption(
                secret="test_secret",
                is_global=True
            )
        ),
        AuthModule,
        UserModule,
        VideoModule
    ],
)
class AppModule:
    ...
