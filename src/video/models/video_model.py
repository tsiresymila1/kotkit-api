import uuid
from typing import TYPE_CHECKING, List, Optional, Annotated

import strawberry
from nestipy_alchemy import sqlalchemy_to_pydantic
from pydantic import Field
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base, s_sq_mapper
from src.comment.models.comment_model import Comment, CommentRelatedModel
from src.like.models.like_model import Like, LikeRelatedModel

if TYPE_CHECKING:
    from src.user.models.user_model import User, UserModel, UserGQL


class Video(Base):
    __tablename__ = 'videos'
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[str] = mapped_column(String(255), ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="videos", init=False, )
    likes: Mapped[list["Like"]] = relationship(
        "Like", back_populates="video", default_factory=lambda: [], )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="video", default_factory=lambda: [], )

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())


VideoModel = sqlalchemy_to_pydantic(Video)


class VideoRelatedModel(VideoModel):
    likes: Optional[List[LikeRelatedModel]] = Field(default=[])
    comments: Optional[List[CommentRelatedModel]] = Field(default=[])
    user: Optional["UserModel"] = Field(default=None)


VideoRelatedModel.model_rebuild(raise_errors=False)


# @s_sq_mapper.type(Video)
# class VideoObject:
#     pass

@strawberry.experimental.pydantic.type(model=VideoModel, all_fields=True)
class VideoGQL:
    user: Annotated["UserGQL", strawberry.lazy("src.user.models.user_model")]
