from dataclasses import dataclass


@dataclass
class CreateCommentDto:
    comment: str
    video_id: str


@dataclass
class UpdateCommentDto(CreateCommentDto):
    id: int