import asyncio
from pathlib import Path
from typing import Annotated
from fastapi import Depends
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from queries.post_queries import PostQueries
from models import Post


class PostPdfService:

    def __init__(
        self,
        read: Annotated[PostQueries, Depends(PostQueries)],
    ):
        self.read = read
        self.media_dir = Path("media/posts-downloads")
        self.media_dir.mkdir(parents=True, exist_ok=True)

    def get_pdf_path(self, post_id: int) -> Path:
        pdf_filename = f"post_{post_id}.pdf"
        return self.media_dir / pdf_filename

    def pdf_exists(self, post_id: int) -> bool:
        return self.get_pdf_path(post_id).exists()

    async def generate_pdf(self, post_id: int) -> Path:
        # Проверка кеша
        pdf_path = self.get_pdf_path(post_id)
        if pdf_path.exists():
            return pdf_path

        post = await self.read.get_by_id(post_id)

        await asyncio.to_thread(self._generate_pdf_sync, post, pdf_path)

        return pdf_path

    def _generate_pdf_sync(self, post: Post, pdf_path: Path) -> None:

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        elements = []
        styles = self._get_pdf_styles()

        # Title
        title = Paragraph(post.title, styles['title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        # Description
        desc_label = Paragraph("<b>Description:</b>", styles['label'])
        elements.append(desc_label)
        description = Paragraph(post.description or "No description", styles['content'])
        elements.append(description)
        elements.append(Spacer(1, 0.1 * inch))

        # Category
        cat_label = Paragraph("<b>Category:</b>", styles['label'])
        elements.append(cat_label)
        category = Paragraph(post.category.name, styles['content'])
        elements.append(category)
        elements.append(Spacer(1, 0.1 * inch))

        # Tags
        tags_label = Paragraph("<b>Tags:</b>", styles['label'])
        elements.append(tags_label)
        if post.tags:
            tags_text = ", ".join([tag.name for tag in post.tags])
        else:
            tags_text = "No tags"
        tags = Paragraph(tags_text, styles['content'])
        elements.append(tags)

        doc.build(elements)

    def _get_pdf_styles(self):
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2c3e50',
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        label_style = ParagraphStyle(
            'Label',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#34495e',
            spaceAfter=6,
            spaceBefore=12,
        )

        content_style = ParagraphStyle(
            'Content',
            parent=styles['BodyText'],
            fontSize=12,
            textColor='#000000',
            spaceAfter=12,
            alignment=TA_LEFT,
        )

        return {
            'title': title_style,
            'label': label_style,
            'content': content_style,
        }
