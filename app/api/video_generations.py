from typing import Annotated, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from config import settings
from models import VideoGenerationStatus
from schemas.video_generation_schema import (
    VideoGenerationUploadResponse,
    VideoGenerationRead,
)
from service.video_generation_service import VideoGenerationService
import uuid
from pathlib import Path
from queries.video_generation_queries import VideoGenerationQueries
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Params
from .dependency.paginate import PaginatePage

router = APIRouter(
    tags=["Video Generations"],
    prefix=settings.url.video_generations,
)


IMAGES_DIR = Path(__file__).resolve().parents[1] / "media" / "images"


@router.get("")
async def index(
    read: Annotated[VideoGenerationQueries, Depends(VideoGenerationQueries)],
    params: Annotated[Params, Depends()],
) -> PaginatePage[VideoGenerationRead]:
    return await apaginate(conn=read.session, query=read.get_all_query(), params=params)


@router.get("/{video_id}")
async def show(
    video_id: int,
    read: Annotated[VideoGenerationQueries, Depends(VideoGenerationQueries)],
) -> VideoGenerationRead:
    video_gen = await read.get_one(video_id)
    if not video_gen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video generation with id {video_id} not found",
        )
    return VideoGenerationRead.model_validate(video_gen)


@router.post(
    "/upload",
    response_model=VideoGenerationUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_images(
    video_service: Annotated[VideoGenerationService, Depends(VideoGenerationService)],
    files: List[UploadFile] = File(...),
) -> VideoGenerationUploadResponse:

    if len(files) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 2 images are required to generate a video",
        )

    image_paths = []
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for file in files:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"All files must be images. Got: {file.content_type}",
            )

        original_extension = Path(file.filename or "image.jpg").suffix
        unique_filename = f"{uuid.uuid4()}{original_extension}"
        file_path = IMAGES_DIR / unique_filename
        relative_path = f"images/{unique_filename}"

        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        image_paths.append(relative_path)

    video_id = await video_service.create(image_paths)

    return VideoGenerationUploadResponse(
        id=video_id,
        status=VideoGenerationStatus.pending,
        image_paths=image_paths,
    )
