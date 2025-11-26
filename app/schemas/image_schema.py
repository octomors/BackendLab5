from pydantic import BaseModel, computed_field

from config import settings


class ProcessedFilesRead(BaseModel):
    grayscale: str
    contrast: str
    blur: str
    sharpen: str
    edges: str

    @computed_field
    @property
    def grayscale_url(self) -> str:
        return f"{settings.run.app_url}/static/{self.grayscale}"

    @computed_field
    @property
    def contrast_url(self) -> str:
        return f"{settings.run.app_url}/static/{self.contrast}"

    @computed_field
    @property
    def blur_url(self) -> str:
        return f"{settings.run.app_url}/static/{self.blur}"

    @computed_field
    @property
    def sharpen_url(self) -> str:
        return f"{settings.run.app_url}/static/{self.sharpen}"

    @computed_field
    @property
    def edges_url(self) -> str:
        return f"{settings.run.app_url}/static/{self.edges}"


class ImageRead(BaseModel):
    id: int
    path: str
    processed_files: ProcessedFilesRead

    @computed_field
    @property
    def full_path(self) -> str:
        return f"{settings.run.app_url}/static/{self.path}"


class ImageUploadResponse(BaseModel):
    id: int
    status: str
    path: str

    @computed_field
    @property
    def full_path(self) -> str:
        return f"{settings.run.app_url}/static/{self.path}"

    class Config:
        from_attributes = True
