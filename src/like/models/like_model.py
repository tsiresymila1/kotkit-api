import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base

if TYPE_CHECKING:
    from src.user.models.user_model import User
    from src.video.models.video_model import Video


class Like(Base):
    __tablename__ = 'likes'

    user_id: Mapped[str] = mapped_column(String(255), ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="likes")

    video_id: Mapped[str] = mapped_column(String(255), ForeignKey('videos.id'))
    video: Mapped["Video"] = relationship("Video", back_populates="likes")

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())
