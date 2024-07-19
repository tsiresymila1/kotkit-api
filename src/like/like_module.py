from nestipy.common import Module

from .like_service import LikeService
from .like_controller import LikeController


@Module(
    providers=[LikeService],
    controllers=[LikeController]
)
class LikeModule:
    ...