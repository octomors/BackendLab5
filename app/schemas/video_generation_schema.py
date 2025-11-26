from pydantic import BaseModel, computed_field
from typing import Optional

from config import settings
from models import VideoGenerationStatus


class VideoGenerationCreate(BaseModel):
    image_paths: list[str]


class VideoGenerationRead(BaseModel):
    id: int
    status: VideoGenerationStatus
    image_paths: list[str]
    video_path: Optional[str]
    error_message: Optional[str]

    @computed_field
    @property
    def image_urls(self) -> list[str]:
        return [f"{settings.run.app_url}/static/{path}" for path in self.image_paths]

    @computed_field
    @property
    def video_url(self) -> Optional[str]:
        if self.video_path:
            return f"{settings.run.app_url}/static/{self.video_path}"
        return None

    class Config:
        from_attributes = True


class VideoGenerationUploadResponse(BaseModel):
    id: int
    status: VideoGenerationStatus
    image_paths: list[str]

    @computed_field
    @property
    def image_urls(self) -> list[str]:
        return [f"{settings.run.app_url}/static/{path}" for path in self.image_paths]

    class Config:
        from_attributes = True
