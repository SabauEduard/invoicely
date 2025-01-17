"""Category type changed to enum

Revision ID: f19374d46a6e
Revises: 019e0bb83b4c
Create Date: 2025-01-13 11:36:16.410128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f19374d46a6e'
down_revision: Union[str, None] = '019e0bb83b4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'category',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.Enum('CONSUMABLES', 'ELECTRICITY', 'IT', 'OTHER', 'PHONE', 'REPAIRS', name='invoicecategory'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'category',
               existing_type=sa.Enum('CONSUMABLES', 'ELECTRICITY', 'IT', 'OTHER', 'PHONE', 'REPAIRS', name='invoicecategory'),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
