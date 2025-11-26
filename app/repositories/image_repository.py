from models import Image, SessionDep


class ImageRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def save(self, image: Image) -> None:
        self.session.add(image)

    async def get_one(self, image_id: int) -> Image | None:
        return await self.session.get(Image, image_id)

    async def delete(self, image: Image) -> None:
        await self.session.delete(image)
