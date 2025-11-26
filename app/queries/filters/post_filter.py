from typing import Optional
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from models import Post, Category, Tag


class CategoryFilter(Filter):
    name: Optional[str] = None
    name__ilike: Optional[str] = None

    class Constants(Filter.Constants):
        model = Category


class TagFilter(Filter):
    name: Optional[str] = None
    name__in: Optional[list[str]] = None
    id__in: Optional[list[int]] = None

    class Constants(Filter.Constants):
        model = Tag


class PostFilter(Filter):

    title__ilike: Optional[str] = None
    description__ilike: Optional[str] = None

    category: Optional[CategoryFilter] = FilterDepends(
        with_prefix("category", CategoryFilter)
    )
    tags: Optional[TagFilter] = FilterDepends(
        with_prefix("tags", TagFilter)
    )

    order_by: Optional[list[str]] = ["id"]

    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Post
        search_model_fields = ["title", "description"]
