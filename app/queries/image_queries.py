from sqlalchemy import Select, select
from models import SessionDep, Image, ImageStatus


class ImageQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def get_completed_images_query(self) -> Select[tuple[Image]]:
        return (
            select(Image).order_by(Image.id).where(Image.status == ImageStatus.complete)
        )
