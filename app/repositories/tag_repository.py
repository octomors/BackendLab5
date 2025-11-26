from models import Tag, SessionDep


class TagRepository:
    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def save(self, tag: Tag) -> None:
        self.session.add(tag)

    async def delete(self, tag: Tag) -> None:
        await self.session.delete(tag)
