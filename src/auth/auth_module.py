from nestipy.common import Module

from .auth_service import AuthService
from .auth_controller import AuthController
from .auth_resolver import AuthResolver


@Module(
    providers=[AuthService, AuthResolver],
    controllers=[AuthController]
)
class AuthModule:
    ...
