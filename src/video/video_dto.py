from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class CreateVideoDto:
    title: str
    description: str
    video: UploadFile


@dataclass
class UpdateVideoDto(CreateVideoDto):
    id: int


@dataclass
class CommentDto:
    comment: str
