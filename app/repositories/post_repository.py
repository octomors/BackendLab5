from models import Post, SessionDep


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
