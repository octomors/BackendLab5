from typing import TypeVar
from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields


T = TypeVar("T")

PaginatePage = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(10, ge=1, le=100),
    ),
]
