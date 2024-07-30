import uuid

from sqlalchemy import String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base, s_sq_mapper, p_sq_mapper
from src.comment.models.comment_model import Comment
from src.like.models.like_model import Like
from src.video.models.video_model import Video


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    videos: Mapped[list[Video]] = relationship("Video", back_populates="user", default_factory=lambda: [])
    comments: Mapped[list[Comment]] = relationship(
        "Comment",
        back_populates="user",
        default_factory=lambda: []
    )
    likes: Mapped[list[Like]] = relationship("Like", back_populates="user", default_factory=lambda: [])

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())


s_sq_mapper.type(User)(type("User", (), {"__exclude__": ["password"]}))
s_sq_mapper.finalize()
p_sq_mapper.type(User, exclude=["password"])(type("User", (), {}))
