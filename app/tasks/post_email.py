from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from task_queue import broker
from models import db_helper, Post
from mailing import get_mail, Mail


@broker.task
async def send_email(
    post_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_helper.session_getter),
    ],
    mail: Annotated[
        Mail,
        TaskiqDepends(get_mail),
    ],
) -> None:
    post = await session.get(Post, post_id)
    await mail.send("test@test.com", "New Post", post.description)
