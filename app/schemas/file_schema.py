from pydantic import BaseModel


class UploadedFile(BaseModel):
    path: str
