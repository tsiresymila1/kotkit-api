from nestipy.common import Injectable

from .like_dto import CreateLikeDto, UpdateLikeDto


@Injectable()
class LikeService:

    async def list(self):
        return "test"

    async def create(self, data: CreateLikeDto):
        return "test"

    async def update(self, id: int, data: UpdateLikeDto):
        return "test"

    async def delete(self, id: int):
        return "test"