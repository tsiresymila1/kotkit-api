from typing import Annotated, cast

from nestipy.graphql import Resolver, Mutation
from nestipy.ioc import Inject, Arg

from .auth_dto import LoginDto, RegisterDto
from .auth_input import LoginInput, RegisterInput
from .auth_service import AuthService
from .models.token import TokenResponse


@Resolver()
class AuthResolver:
    auth_service: Annotated[AuthService, Inject()]

    @Mutation()
    async def login(self, data: Annotated[LoginInput, Arg()]) -> TokenResponse:
        print("Login data :::", data)
        token_dict = await self.auth_service.login(cast(LoginDto, data))
        return TokenResponse(token=token_dict["token"])

    @Mutation()
    async def register(self, data: Annotated[RegisterInput, Arg()]) -> TokenResponse:
        token_dict = await self.auth_service.register(cast(RegisterDto, data))
        return TokenResponse(token=token_dict["token"])
