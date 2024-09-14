import uuid
from typing import TYPE_CHECKING

from nestipy_alchemy.converter import AlchemyPydanticMixim
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from base_model import Base

if TYPE_CHECKING:
    from src.user.models.user_model import User


class Follow(Base, AlchemyPydanticMixim):
    __tablename__ = 'follows'

    user_id: Mapped[str] = mapped_column(String(255), ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="followers", foreign_keys=[user_id])

    following_id: Mapped[str] = mapped_column(String(255), ForeignKey('users.id'))
    following: Mapped["User"] = relationship("User", back_populates="following", foreign_keys=[following_id])

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default_factory=lambda: uuid.uuid4().hex)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default_factory=lambda: func.now(), onupdate=func.now())
