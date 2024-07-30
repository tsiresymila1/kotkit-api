from typing import Annotated

from nestipy.graphql import Resolver, Query
from nestipy.ioc import Inject

from base_model import s_sq_mapper
from .user_service import UserService
from ..auth.auth_guards import Auth

User = s_sq_mapper.mapped_types.get("User")


@Auth()
@Resolver()
class UserResolver:
    user_service: Annotated[UserService, Inject()]

    @Query()
    async def list_user(self) -> list[User]:
        return await self.user_service.list()
