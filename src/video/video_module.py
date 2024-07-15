from nestipy.common import Module

from .video_service import VideoService
from .video_controller import VideoController


@Module(
    providers=[VideoService],
    controllers=[VideoController]
)
class VideoModule:
    ...