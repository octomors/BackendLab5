from typing import Annotated
from fastapi import Depends
from models import SessionDep, Image, ImageStatus
from repositories.image_repository import ImageRepository
from schemas.file_schema import UploadedFile
from tasks.image_gen import image_variants


class ImageService:

    def __init__(
        self,
        uow: SessionDep,
        image_repository: Annotated[ImageRepository, Depends(ImageRepository)],
    ):
        self.uow = uow
        self.image_repository = image_repository

    async def create(self, uploaded_file: UploadedFile) -> int:
        image = Image(
            status=ImageStatus.pending,
            path=uploaded_file.path,
            processed_files=None,
            error_message=None,
        )
        self.image_repository.save(image)
        await self.uow.commit()

        await image_variants.kiq(image_id=image.id)

        return image.id
