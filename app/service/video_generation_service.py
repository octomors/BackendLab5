from typing import Annotated
from fastapi import Depends
from models import SessionDep, VideoGeneration, VideoGenerationStatus
from repositories.video_generation_repository import VideoGenerationRepository
from tasks.video_gen import generate_video


class VideoGenerationService:

    def __init__(
        self,
        uow: SessionDep,
        video_repository: Annotated[
            VideoGenerationRepository, Depends(VideoGenerationRepository)
        ],
    ):
        self.uow = uow
        self.video_repository = video_repository

    async def create(self, image_paths: list[str]) -> int:
        video_gen = VideoGeneration(
            status=VideoGenerationStatus.pending,
            image_paths=image_paths,
            video_path=None,
            error_message=None,
        )
        self.video_repository.save(video_gen)
        await self.uow.commit()

        await generate_video.kiq(video_id=video_gen.id)

        return video_gen.id
