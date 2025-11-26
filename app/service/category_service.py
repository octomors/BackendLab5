from typing import Annotated
from fastapi import Depends
from repositories.category_repository import CategoryRepository
from queries.category_queries import CategoryQueries
from queries.post_queries import PostQueries
from schemas.category_schema import CategoryCreate, CategoryUpdate
from models import Category, SessionDep
from exceptions import CategoryNotFoundException
from exceptions import CategoryHasPostsException


class CategoryService:
    def __init__(
        self,
        uow: SessionDep,
        post_queries: Annotated[
            PostQueries,
            Depends(PostQueries),
        ],
        category_queries: Annotated[
            CategoryQueries,
            Depends(CategoryQueries),
        ],
        category_repository: Annotated[
            CategoryRepository,
            Depends(CategoryRepository),
        ],
    ):
        self.uow = uow
        self.category_queries = category_queries
        self.category_repository = category_repository
        self.post_queries = post_queries

    async def create(self, category_create: CategoryCreate) -> int:

        category = Category(name=category_create.name)

        self.category_repository.save(category)
        await self.uow.commit()

        return category.id

    async def update(self, category_id: int, category_update: CategoryUpdate) -> int:
        category = await self.category_queries.get_one(category_id)
        if not category:
            raise CategoryNotFoundException()

        category.name = category_update.name
        await self.uow.commit()
        return category.id

    async def destroy(self, id: int) -> None:
        category = await self.category_queries.get_one(id)

        if not category:
            raise CategoryNotFoundException()

        if await self.post_queries.has_by_category(category.id):
            raise CategoryHasPostsException()

        await self.category_repository.delete(category)
        await self.uow.commit()
