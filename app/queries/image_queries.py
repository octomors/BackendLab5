from sqlalchemy import Select, select
from models import SessionDep, Image, ImageStatus


class ImageQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    async def get_one(self, image_id: int) -> Image | None:
        return await self.session.get(Image, image_id)

    def get_completed_images_query(self) -> Select[tuple[Image]]:
        return (
            select(Image).order_by(Image.id).where(Image.status == ImageStatus.complete)
        )
