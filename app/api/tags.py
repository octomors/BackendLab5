from typing import Annotated
from fastapi import APIRouter, Depends, status
from models import Tag, SessionDep
from pydantic import BaseModel
from config import settings
from queries.tag_queries import TagQueries
from repositories.tag_repository import TagRepository
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Params
from .dependency.paginate import PaginatePage

router = APIRouter(
    tags=["Tags"],
    prefix=settings.url.tags,
)


class TagRead(BaseModel):
    id: int
    name: str


class TagCreate(BaseModel):
    name: str


@router.get("")
async def index(
    read: Annotated[TagQueries, Depends(TagQueries)],
    params: Annotated[Params, Depends()],
) -> PaginatePage[TagRead]:
    return await apaginate(
        conn=read.session, query=read.get_tags_query(), params=params
    )


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def store(
    uow: SessionDep,
    tag_repository: Annotated[TagRepository, Depends(TagRepository)],
    tag_create: TagCreate,
):
    tag = Tag(name=tag_create.name)
    tag_repository.save(tag)
    await uow.commit()
    return tag
