from nestipy.common import Module

from .comment_service import CommentService
from .comment_controller import CommentController


@Module(
    providers=[CommentService],
    controllers=[CommentController]
)
class CommentModule:
    ...