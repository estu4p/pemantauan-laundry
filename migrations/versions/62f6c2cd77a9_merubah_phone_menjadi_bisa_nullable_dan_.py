"""merubah phone menjadi bisa nullable dan bukan unique

Revision ID: 62f6c2cd77a9
Revises: 7d26c139d502
Create Date: 2024-04-22 10:21:59.515358

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '62f6c2cd77a9'
down_revision = '7d26c139d502'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
        batch_op.drop_index('phone')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.create_index('phone', ['phone'], unique=True)
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###
