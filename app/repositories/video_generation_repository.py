from models import VideoGeneration, SessionDep


class VideoGenerationRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def save(self, video_generation: VideoGeneration) -> None:
        self.session.add(video_generation)

    async def delete(self, video_generation: VideoGeneration) -> None:
        await self.session.delete(video_generation)
