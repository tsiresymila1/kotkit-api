from dataclasses import dataclass


@dataclass
class CreateLikeDto:
    video_id: str


@dataclass
class UpdateLikeDto(CreateLikeDto):
    id: int
