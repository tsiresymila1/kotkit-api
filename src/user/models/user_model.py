import uuid

from sqlalchemy import String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from nestipy_alchemy.converter import AlchemyPydanticMixim
from base_model import Base, s_sq_mapper
from src.comment.models.comment_model import Comment
from src.follow.models.follow_model import Follow
from src.like.models.like_model import Like
from src.video.models.video_model import Video


class User(Base, AlchemyPydanticMixim):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

    videos: Mapped[list[Video]] = relationship("Video", back_populates="user", default_factory=lambda: [])
    comments: Mapped[list[Comment]] = relationship(
        "Comment",
        back_populates="user",
        default_factory=lambda: []
    )
    likes: Mapped[list[Like]] = relationship("Like", back_populates="user", default_factory=lambda: [])
    followers: Mapped[list[Follow]] = relationship(
        "Follow",
        back_populates="user",
        default_factory=lambda: [],
        foreign_keys=[Follow.user_id]
    )
    following: Mapped[list[Follow]] = relationship(
        "Follow",
        back_populates="following",
        default_factory=lambda: [],
        foreign_keys=[Follow.following_id]
    )
    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())


s_sq_mapper.type(User)(type("User", (), {"__exclude__": ["password"]}))
s_sq_mapper.finalize()
User.load(exclude=["password"], model_name="User")
