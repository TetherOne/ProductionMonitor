"""connection shift_task and product_code

Revision ID: 3fede1f10a25
Revises: f4d15015df13
Create Date: 2025-05-14 08:04:21.579636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fede1f10a25"
down_revision: Union[str, None] = "f4d15015df13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "product_codes", sa.Column("shift_task_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        None, "product_codes", "shift_tasks", ["shift_task_id"], ["id"]
    )
    op.create_unique_constraint(
        "uq_batch_number_date", "shift_tasks", ["batch_number", "batch_date"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_batch_number_date", "shift_tasks", type_="unique")
    op.drop_constraint(None, "product_codes", type_="foreignkey")
    op.drop_column("product_codes", "shift_task_id")
