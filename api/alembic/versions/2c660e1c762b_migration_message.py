"""migration message

Revision ID: 2c660e1c762b
Revises: f19374d46a6e
Create Date: 2025-01-13 17:52:37.179094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '2c660e1c762b'
down_revision: Union[str, None] = 'f19374d46a6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'importance',
               existing_type=mysql.INTEGER(),
               type_=sa.Enum('LOW', 'MEDIUM', 'HIGH', name='importance'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'importance',
               existing_type=sa.Enum('LOW', 'MEDIUM', 'HIGH', name='importance'),
               type_=mysql.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
