from models import Tag, SessionDep
from sqlalchemy import select
from typing import Sequence


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

    async def get_one(self, id: int) -> Tag | None:
        return await self.session.get(Tag, id)

    async def get_many_by_names(self, names: list[str]) -> Sequence[Tag]:
        if not names:
            return []
        tags = await self.session.scalars(select(Tag).where(Tag.name.in_(names)))
        return tags.all()

    async def get_many(self, ids: list[int]) -> Sequence[Tag]:
        if not ids:
            return []
        tags = await self.session.scalars(select(Tag).where(Tag.id.in_(ids)))
        return tags.all()
