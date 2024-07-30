import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base

if TYPE_CHECKING:
    from src.user.models.user_model import User
    from src.video.models.video_model import Video


class Comment(Base):
    __tablename__ = 'comments'

    text: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[str] = mapped_column(String(255), ForeignKey('users.id'))
    video_id: Mapped[str] = mapped_column(String(255), ForeignKey('videos.id'))
    user: Mapped["User"] = relationship("User", back_populates="comments", default=None)

    video: Mapped["Video"] = relationship("Video", back_populates="comments", default=None)

    parent_id: Mapped[str] = mapped_column(String(255), ForeignKey('comments.id'), default=None)

    replies: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="parent", default_factory=lambda: [])

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)

    parent: Mapped["Comment"] = relationship(
        "Comment", back_populates="replies", remote_side=[id], default=None)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())
