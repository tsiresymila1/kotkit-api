from nestipy.common import Module

from .user_service import UserService
from .user_controller import UserController
from .user_resolver import UserResolver


@Module(
    providers=[
        UserService,
        UserResolver
    ],
    controllers=[UserController]
)
class UserModule:
    ...
