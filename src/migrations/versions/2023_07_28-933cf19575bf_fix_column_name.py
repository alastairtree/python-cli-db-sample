"""Fix column name

Revision ID: 933cf19575bf
Revises: 0a59bacb83a8
Create Date: 2023-07-28 17:22:49.709090

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "933cf19575bf"
down_revision = "0a59bacb83a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("user_account", column_name="fullname2", new_column_name="fullname")
    pass


def downgrade() -> None:
    op.alter_column("user_account", column_name="fullname", new_column_name="fullname2")
    pass
