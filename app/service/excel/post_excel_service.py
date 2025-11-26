from datetime import datetime
from io import BytesIO
from typing import Annotated
from fastapi import Depends
from openpyxl import Workbook

from schemas.excel_schema import ExcelExportResult
from queries.filters.post_filter import PostFilter
from queries.post_queries import PostQueries


class PostExcelService:

    def __init__(
        self,
        read: Annotated[PostQueries, Depends(PostQueries)],
    ):
        self.read = read

    async def generate(
        self,
        filter: PostFilter,
        chunk_size: int = 500,
    ) -> ExcelExportResult:
        stream = BytesIO()
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Posts"

        worksheet.append(["ID", "Title", "Description", "Category", "Tags"])

        async for post in self.read.stream(filter, chunk_size=chunk_size):
            tags = ", ".join(tag.name for tag in post.tags) if post.tags else ""
            worksheet.append([
                post.id,
                post.title,
                post.description or "",
                post.category.name if post.category else "",
                tags,
            ])

        workbook.save(stream)
        stream.seek(0)

        filename = f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return ExcelExportResult(content=stream, filename=filename)
