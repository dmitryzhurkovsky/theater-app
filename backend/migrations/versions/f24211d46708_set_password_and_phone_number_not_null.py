"""Set password and phone number to not null

Revision ID: f24211d46708
Revises: c7d5900a949a
Create Date: 2024-07-08 15:28:14.203039

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f24211d46708"
down_revision = "c7d5900a949a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", "phone_number", existing_type=sa.String(), nullable=True)
    op.alter_column("users", "password", existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    op.alter_column("users", "password", existing_type=sa.String(), nullable=False)
    op.alter_column("users", "phone_number", existing_type=sa.String(), nullable=False)
