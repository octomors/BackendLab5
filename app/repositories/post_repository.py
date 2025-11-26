from models import Post, SessionDep
from sqlalchemy import select, exists


class PostRepository:
    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def save(self, post: Post) -> None:
        self.session.add(post)

    async def delete(self, post: Post) -> None:
        await self.session.delete(post)

    async def get_one(self, id: int) -> Post | None:
        return await self.session.get(Post, id)

    async def has_by_category(self, category_id: int) -> bool:
        return await self.session.scalar(
            select(exists().where(Post.category_id == category_id))
        )
