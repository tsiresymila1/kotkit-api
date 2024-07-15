from nestipy.common import Module

from .auth_service import AuthService
from .auth_controller import AuthController


@Module(
    providers=[AuthService],
    controllers=[AuthController]
)
class AuthModule:
    ...