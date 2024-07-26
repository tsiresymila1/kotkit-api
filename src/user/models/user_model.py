import uuid
from typing import Optional, List

import strawberry
from nestipy_alchemy import sqlalchemy_to_pydantic
from pydantic import Field
from sqlalchemy import String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base, s_sq_mapper
from src.comment.models.comment_model import Comment, CommentRelatedModel
from src.like.models.like_model import Like, LikeRelatedModel
from src.video.models.video_model import Video, VideoModel, VideoRelatedModel


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    videos: Mapped[list[Video]] = relationship("Video", back_populates="user", default_factory=lambda: [])
    comments: Mapped[list[Comment]] = relationship("Comment", back_populates="user", default_factory=lambda: [])
    likes: Mapped[list[Like]] = relationship("Like", back_populates="user", default_factory=lambda: [])

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())


UserModel = sqlalchemy_to_pydantic(User, exclude=["password"])


class UserRelatedVideoModel(UserModel):
    videos: Optional[List[VideoModel]] = Field(default=[])


class UserRelatedModel(UserModel):
    videos: Optional[List[VideoRelatedModel]] = Field(default=[])
    likes: Optional[List[LikeRelatedModel]] = Field(default=[])
    comments: Optional[List[CommentRelatedModel]] = Field(default=[])


UserRelatedModel.model_rebuild()


# @s_sq_mapper.type(User)
# class UserObject:
#     __exclude__ = ["password"]

@strawberry.experimental.pydantic.type(model=UserModel, all_fields=True)
class UserGQL:
    pass
