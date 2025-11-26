from sqlalchemy import Select, select
from models import SessionDep, VideoGeneration


class VideoGenerationQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    async def get_one(self, video_id: int) -> VideoGeneration | None:
        return await self.session.get(VideoGeneration, video_id)

    def get_all_query(self) -> Select[tuple[VideoGeneration]]:
        return select(VideoGeneration).order_by(VideoGeneration.id)
