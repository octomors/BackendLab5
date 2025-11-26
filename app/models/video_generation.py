import enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class VideoGenerationStatus(enum.Enum):
    pending = "pending"
    success = "success"
    error = "error"


class VideoGeneration(Base):

    __tablename__ = "video_generations"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[VideoGenerationStatus] = mapped_column(
        SQLAEnum(
            VideoGenerationStatus, name="video_generation_status", create_constraint=True
        ),
        nullable=False,
        index=True,
        default=VideoGenerationStatus.pending,
    )

    image_paths: Mapped[list] = mapped_column(JSON, nullable=False)

    video_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"VideoGeneration(id={self.id}, status={self.status.value})"
