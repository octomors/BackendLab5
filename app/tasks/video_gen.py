from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from task_queue import broker
from models import db_helper, VideoGeneration, VideoGenerationStatus
from pathlib import Path
import uuid

MEDIA_DIR = Path(__file__).resolve().parents[1] / "media"


@broker.task
async def generate_video(
    video_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
) -> None:
    video_gen = await session.get(VideoGeneration, video_id)

    if not video_gen:
        return

    try:
        video_path = create_video_from_images(video_gen.image_paths)
        video_gen.status = VideoGenerationStatus.success
        video_gen.video_path = video_path
        video_gen.error_message = None

    except Exception as e:
        video_gen.status = VideoGenerationStatus.error
        video_gen.error_message = str(e)

    await session.commit()


def create_video_from_images(image_paths: list[str]) -> str:
    from moviepy import ImageClip, concatenate_videoclips

    clips = []
    for img_path in image_paths:
        full_path = MEDIA_DIR / img_path
        if not full_path.exists():
            raise FileNotFoundError(f"Image not found: {img_path}")

        clip = ImageClip(str(full_path)).with_duration(2)
        clips.append(clip)

    if not clips:
        raise ValueError("No images provided for video generation")

    final_clip = concatenate_videoclips(clips, method="compose")

    videos_dir = MEDIA_DIR / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    video_filename = f"{uuid.uuid4()}.mp4"
    video_full_path = videos_dir / video_filename
    relative_path = f"videos/{video_filename}"

    final_clip.write_videofile(
        str(video_full_path),
        fps=24,
        codec="libx264",
        audio=False,
    )

    final_clip.close()
    for clip in clips:
        clip.close()

    return relative_path
