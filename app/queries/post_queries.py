from typing import AsyncIterator
from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from exceptions import PostNotFoundException
from models import Post, SessionDep
from queries.filters.post_filter import PostFilter


class PostQueries:

    def __init__(
        self,
        session: SessionDep,
    ):
        self.session = session

    def get_posts_query(self) -> Select[tuple[Post]]:
        return (
            select(Post)
            .outerjoin(Post.category)
            .outerjoin(Post.tags)
            .options(contains_eager(Post.category))
            .options(contains_eager(Post.tags))
            .distinct()
        )

    def filtered_query(self, filter: PostFilter) -> Select[tuple[Post]]:
        query = self.get_posts_query()
        query = filter.filter(query)
        query = filter.sort(query)
        return query

    async def get_by_id(self, post_id: int) -> Post | None:
        post = await self.session.get(
            Post, post_id, options=[selectinload(Post.tags), joinedload(Post.category)]
        )
        if not post:
            raise PostNotFoundException()
        # В идеале возвращать DTO, а не модель
        return post

    async def stream(
        self,
        filter: PostFilter,
        chunk_size: int = 500,
    ) -> AsyncIterator[Post]:
        query = self.filtered_query(filter).execution_options(stream_results=True)
        result = await self.session.stream_scalars(query)
        result = result.unique()
        async for post in result.yield_per(chunk_size):
            yield post
