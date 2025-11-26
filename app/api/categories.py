from typing import Annotated
from fastapi import APIRouter, Depends, status
from config import settings
from service.category_service import CategoryService
from schemas.category_schema import CategoryUpdate, CategoryCreate, CategoryRead
from queries.category_queries import CategoryQueries
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Params
from .dependency.paginate import PaginatePage

router = APIRouter(
    tags=["Categories"],
    prefix=settings.url.categories,
)


@router.get("")
async def index(
    read: Annotated[CategoryQueries, Depends(CategoryQueries)],
    params: Annotated[Params, Depends()],
) -> PaginatePage[CategoryRead]:
    return await apaginate(
        conn=read.session, query=read.get_categories_query(), params=params
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def store(
    category_create: CategoryCreate,
    category_service: Annotated[CategoryService, Depends(CategoryService)],
):
    category_id = await category_service.create(category_create)
    return category_id


@router.put("/{id}")
async def update(
    service: Annotated[CategoryService, Depends(CategoryService)],
    id: int,
    category_update: CategoryUpdate,
) -> int:
    category_id = await service.update(id, category_update)
    return category_id


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    service: Annotated[CategoryService, Depends(CategoryService)],
    id: int,
):
    await service.destroy(id)
    return None
