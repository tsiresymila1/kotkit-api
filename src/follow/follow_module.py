from nestipy.common import Module

from .follow_service import FollowService
from .follow_controller import FollowController


@Module(
    providers=[FollowService],
    controllers=[FollowController]
)
class FollowModule:
    ...