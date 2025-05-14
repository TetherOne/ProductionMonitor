"""shift_task and product_code

Revision ID: f4d15015df13
Revises:
Create Date: 2025-05-14 08:00:48.627093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4d15015df13"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product_codes",
        sa.Column("unique_code", sa.String(), nullable=False),
        sa.Column("is_aggregated", sa.Boolean(), nullable=False),
        sa.Column("aggregated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_codes_unique_code"),
        "product_codes",
        ["unique_code"],
        unique=True,
    )
    op.create_table(
        "shift_tasks",
        sa.Column("task_representation", sa.String(), nullable=False),
        sa.Column("work_center", sa.String(), nullable=False),
        sa.Column("shift", sa.String(), nullable=False),
        sa.Column("brigade", sa.String(), nullable=False),
        sa.Column("batch_number", sa.Integer(), nullable=False),
        sa.Column("batch_date", sa.Date(), nullable=False),
        sa.Column("nomenclature", sa.String(), nullable=False),
        sa.Column("code_ekn", sa.String(), nullable=False),
        sa.Column("rc_identifier", sa.String(), nullable=False),
        sa.Column("shift_start", sa.DateTime(), nullable=False),
        sa.Column("shift_end", sa.DateTime(), nullable=False),
        sa.Column("is_closed", sa.Boolean(), nullable=False),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("shift_tasks")
    op.drop_index(op.f("ix_product_codes_unique_code"), table_name="product_codes")
    op.drop_table("product_codes")
