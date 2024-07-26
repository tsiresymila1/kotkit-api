from nestipy.common import Module

from .video_service import VideoService
from .video_controller import VideoController
from .video_resolver import VideoResolver


@Module(
    providers=[
        VideoService,
        VideoResolver
    ],
    controllers=[VideoController]
)
class VideoModule:
    ...
