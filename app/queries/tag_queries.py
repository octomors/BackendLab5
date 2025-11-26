from typing import Sequence
from sqlalchemy import Select, select
from models import SessionDep, Tag


class TagQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def get_tags_query(self) -> Select[tuple[Tag]]:
        return select(Tag).order_by(Tag.id)

    async def get_by_id(self, tag_id: int) -> Tag | None:
        return await self.session.get(Tag, tag_id)

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
