"""Change status to string

Revision ID: a4b0980c6575
Revises: 4e832d79bdef
Create Date: 2025-03-20 00:17:49.599437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4b0980c6575'
down_revision: Union[str, None] = '4e832d79bdef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('report_card_content', 'status',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Enum('PRIVATE', 'PUBLIC', 'FRIENDS_ONLY', name='report_status'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('report_card_content', 'status',
               existing_type=sa.Enum('PRIVATE', 'PUBLIC', 'FRIENDS_ONLY', name='report_status'),
               type_=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###
