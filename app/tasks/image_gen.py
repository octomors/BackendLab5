# Уточнить нормально ли работать в задаче без репо и read model

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from task_queue import broker
from models import db_helper, Image, ImageStatus
from pathlib import Path
from PIL import Image as PILImage, ImageEnhance, ImageFilter

MEDIA_DIR = Path(__file__).resolve().parents[1] / "media"


@broker.task
async def image_variants(
    image_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
) -> None:
    image = await session.get(Image, image_id)

    full_path = MEDIA_DIR / image.path

    try:
        processed_files = process_image_variants(full_path)
        image.status = ImageStatus.complete
        image.processed_files = processed_files
        image.error_message = None

    except Exception as e:
        image.status = ImageStatus.error
        image.error_message = str(e)

    await session.commit()


def process_image_variants(source_path: Path) -> dict[str, str]:

    if not source_path.exists():
        raise FileNotFoundError("Файл не найден")

    with PILImage.open(source_path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        stem = source_path.stem
        extension = source_path.suffix
        output_dir = source_path.parent

        processed = {}

        # Grayscale
        grayscale_filename = f"{stem}__grayscale{extension}"
        grayscale_path = output_dir / grayscale_filename
        grayscale_img = img.convert("L")
        grayscale_img.save(grayscale_path)
        processed["grayscale"] = f"images/{grayscale_filename}"

        # Увеличенный контраст
        contrast_filename = f"{stem}__contrast{extension}"
        contrast_path = output_dir / contrast_filename
        enhancer = ImageEnhance.Contrast(img)
        contrast_img = enhancer.enhance(2.0)
        contrast_img.save(contrast_path)
        processed["contrast"] = f"images/{contrast_filename}"

        # Blur
        blur_filename = f"{stem}__blur{extension}"
        blur_path = output_dir / blur_filename
        blur_img = img.filter(ImageFilter.GaussianBlur(radius=5))
        blur_img.save(blur_path)
        processed["blur"] = f"images/{blur_filename}"

        # Sharpen
        sharpen_filename = f"{stem}__sharpen{extension}"
        sharpen_path = output_dir / sharpen_filename
        sharpen_img = img.filter(ImageFilter.SHARPEN)
        sharpen_img.save(sharpen_path)
        processed["sharpen"] = f"images/{sharpen_filename}"

        # Edge Detection
        edges_filename = f"{stem}__edges{extension}"
        edges_path = output_dir / edges_filename
        edges_img = img.filter(ImageFilter.FIND_EDGES)
        edges_img.save(edges_path)
        processed["edges"] = f"images/{edges_filename}"

    return processed
