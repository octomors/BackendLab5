from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from config import settings
from models import ImageStatus
from schemas.file_schema import UploadedFile
from schemas.image_schema import ImageUploadResponse, ImageRead
from service.image_service import ImageService
import uuid
from pathlib import Path
from queries.image_queries import ImageQueries
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Params
from .dependency.paginate import PaginatePage

router = APIRouter(
    tags=["Images"],
    prefix=settings.url.images,
)


IMAGES_DIR = Path(__file__).resolve().parents[1] / "media" / "images"


@router.get("")
async def index(
    read: Annotated[ImageQueries, Depends(ImageQueries)],
    params: Annotated[Params, Depends()],
) -> PaginatePage[ImageRead]:
    return await apaginate(
        conn=read.session, query=read.get_completed_images_query(), params=params
    )


@router.post(
    "/upload",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    image_service: Annotated[ImageService, Depends(ImageService)],
    file: UploadFile = File(...),
) -> ImageUploadResponse:

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Файл должен быть изображением. Получен тип: {file.content_type}",
        )

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    original_extension = Path(file.filename or "image.jpg").suffix
    unique_filename = f"{uuid.uuid4()}{original_extension}"
    file_path = IMAGES_DIR / unique_filename
    relative_path = f"images/{unique_filename}"

    contents = file.file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    uploaded_file = UploadedFile(
        path=relative_path,
    )
    image_id = await image_service.create(uploaded_file)

    return ImageUploadResponse(
        id=image_id,
        status=ImageStatus.pending,
        path=relative_path,
    )
