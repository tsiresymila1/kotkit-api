from dataclasses import dataclass


@dataclass
class CreateLikeDto:
    name: str


@dataclass
class UpdateLikeDto(CreateLikeDto):
    id: int