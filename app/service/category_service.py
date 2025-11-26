from typing import Annotated
from fastapi import Depends
from repositories.category_repository import CategoryRepository
from schemas.category_schema import CategoryCreate, CategoryUpdate
from models import Category, SessionDep
from exceptions import CategoryNotFoundException
from repositories.post_repository import PostRepository
from exceptions import CategoryHasPostsException


class CategoryService:
    def __init__(
        self,
        uow: SessionDep,
        post_repository: Annotated[
            PostRepository,
            Depends(PostRepository),
        ],
        category_repository: Annotated[
            CategoryRepository,
            Depends(CategoryRepository),
        ],
    ):
        self.uow = uow
        self.category_repository = category_repository
        self.post_repository = post_repository

    async def create(self, category_create: CategoryCreate) -> int:

        category = Category(name=category_create.name)

        self.category_repository.save(category)
        await self.uow.commit()

        return category.id

    async def update(self, category_id: int, category_update: CategoryUpdate) -> int:
        category = await self.category_repository.get_one(category_id)
        if not category:
            raise CategoryNotFoundException()

        category.name = category_update.name
        await self.uow.commit()
        return category.id

    async def destroy(self, id: int) -> None:
        category = await self.category_repository.get_one(id)

        if not category:
            raise CategoryNotFoundException()

        if self.post_repository.has_by_category(category.id):
            raise CategoryHasPostsException()

        await self.category_repository.delete(category)
        await self.uow.commit()
