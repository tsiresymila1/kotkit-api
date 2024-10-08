import uuid
from typing import TYPE_CHECKING

from nestipy_alchemy.converter import AlchemyPydanticMixim
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base
from src.comment.models.comment_model import Comment
from src.like.models.like_model import Like

if TYPE_CHECKING:
    from src.user.models.user_model import User


class Video(Base, AlchemyPydanticMixim):
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
