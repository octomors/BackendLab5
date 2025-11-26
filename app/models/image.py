import enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ImageStatus(enum.Enum):
    pending = "pending"
    complete = "complete"
    error = "error"


class Image(Base):

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[ImageStatus] = mapped_column(
        SQLAEnum(ImageStatus, name="image_status", create_constraint=True),
        nullable=False,
        index=True,
        default=ImageStatus.pending,
    )

    path: Mapped[str] = mapped_column(String(512), nullable=False)

    processed_files: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"Image(id={self.id}, status={self.status.value}, path={self.path})"
