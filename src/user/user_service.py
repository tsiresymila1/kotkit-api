from nestipy.common import Injectable
from nestipy.ioc import Inject
from nestipy_alchemy import SQLAlchemyService
from nestipy_jwt.jwt_service import Annotated
from sqlalchemy.future import select
from sqlalchemy.orm import immediateload

from .models.user_model import User, UserRelatedVideoModel
from .user_dto import CreateUserDto, UpdateUserDto


@Injectable()
class UserService:
    db_service: Annotated[SQLAlchemyService, Inject()]

    async def list(self):
        async with self.db_service.session as session:
            stmt = select(User).options(immediateload(User.videos))
            result = await session.execute(stmt)
            users = result.scalars().all()
            users_dict = [
                UserRelatedVideoModel.model_validate(user).model_dump(mode='json') for user in
                users
            ]
            await session.commit()
        return users_dict

    async def create(self, data: CreateUserDto):
        return "test"

    async def update(self, id: int, data: UpdateUserDto):
        return "test"

    async def delete(self, id: int):
        return "test"
