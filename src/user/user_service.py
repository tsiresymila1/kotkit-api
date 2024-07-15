from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_jwt.jwt_service import Annotated
from nestipy_prisma import PrismaService

from .user_dto import CreateUserDto, UpdateUserDto


@Injectable()
class UserService:
    prisma: Annotated[PrismaService, Inject()]

    async def list(self):
        users = await self.prisma.user.find_many()
        return [u.model_dump(mode='json') for u in users]

    async def create(self, data: CreateUserDto):
        return "test"

    async def update(self, id: int, data: UpdateUserDto):
        return "test"

    async def delete(self, id: int):
        return "test"
