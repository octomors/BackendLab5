from pydantic import BaseModel
from schemas.category_schema import CategoryRead
from schemas.tag_schema import TagRead


class PostCategoryRead(BaseModel):
    id: int
    title: str
    description: str
    read_time: int | None
    category: CategoryRead
    tags: list[TagRead]


class PostRead(BaseModel):
    id: int
    title: str
    description: str


class PostUpdate(BaseModel):
    title: str
    description: str
    category_id: int
    tag_ids: list[int]
    tags: list[str]


class PostCreate(BaseModel):
    title: str
    description: str
    category_id: int
    tag_ids: list[int]
    tags: list[str]
