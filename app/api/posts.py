from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, StreamingResponse
from config import settings
from authentication.fastapi_users import current_active_user
from service.post_service import PostService
from service.pdf import PostPdfService
from service.excel import PostExcelService
from schemas.post_schema import PostCreate, PostCategoryRead, PostUpdate
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Params
from queries.filters.post_filter import PostFilter
from fastapi_filter import FilterDepends
from queries.post_queries import PostQueries
from .dependency.paginate import PaginatePage

router = APIRouter(
    tags=["Posts"],
    prefix=settings.url.posts,
)


@router.get("")
async def index(
    filter: Annotated[PostFilter, FilterDepends(PostFilter)],
    params: Annotated[Params, Depends()],
    read: Annotated[PostQueries, Depends(PostQueries)],
) -> PaginatePage[PostCategoryRead]:
    return await apaginate(
        conn=read.session, query=read.filtered_query(filter), params=params
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def store(
    post_create: PostCreate,
    service: Annotated[PostService, Depends(PostService)],
) -> int:
    poist_id = await service.create(post_create)
    return poist_id


@router.get("/{id}", response_model=PostCategoryRead)
async def show(
    id: int,
    read: Annotated[PostQueries, Depends(PostQueries)],
):
    post = await read.get_by_id(id)
    return post


@router.put("/{id}")
async def update(
    service: Annotated[PostService, Depends(PostService)],
    id: int,
    post_update: PostUpdate,
) -> int:
    poist_id = await service.update(id, post_update)
    return poist_id


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    service: Annotated[PostService, Depends(PostService)],
    id: int,
):
    await service.destroy(id)
    return None


@router.get("/{id}/pdf")
async def generate_pdf(
    id: int,
    pdf_service: Annotated[PostPdfService, Depends()],
) -> FileResponse:
    pdf_path = await pdf_service.generate_pdf(id)

    return FileResponse(
        path=pdf_path, media_type="application/pdf", filename=f"post_{id}.pdf"
    )


@router.get("/export/excel")
async def export_excel(
    filter: Annotated[PostFilter, FilterDepends(PostFilter)],
    excel_service: Annotated[PostExcelService, Depends(PostExcelService)],
) -> StreamingResponse:
    result = await excel_service.generate(filter)

    return StreamingResponse(
        result.content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{result.filename}"'},
    )
