"""add video_generations table

Revision ID: a1b2c3d4e5f6
Revises: d264ce70caa7
Create Date: 2025-11-26 18:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "d264ce70caa7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "video_generations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "success",
                "error",
                name="video_generation_status",
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "image_paths",
            postgresql.JSON(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("video_path", sa.String(length=512), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_video_generations_status"), "video_generations", ["status"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_video_generations_status"), table_name="video_generations")
    op.drop_table("video_generations")
