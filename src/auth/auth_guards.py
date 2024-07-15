from typing import Union, Awaitable, Annotated

from nestipy.common import CanActivate, Injectable, apply_decorators, UseGuards
from nestipy.core import ExecutionContext
from nestipy.ioc import Inject
from nestipy.openapi import ApiBearerAuth, ApiOkResponse

from .auth_service import AuthService


@Injectable()
class AuthGuard(CanActivate):
    auth_service: Annotated[AuthService, Inject()]

    async def can_activate(self, context: "ExecutionContext") -> Union[Awaitable[bool], bool]:
        request = context.switch_to_http().get_request()
        token = (request.headers.get('authorization') or '').replace("Bearer ", "")
        user = await self.auth_service.check(token)
        if user:
            request.user = user
            return True
        else:
            return False


def Auth():
    return apply_decorators(
        UseGuards(AuthGuard),
        ApiBearerAuth(),
        ApiOkResponse()
    )
