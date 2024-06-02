"""menambah price di customer

Revision ID: 375ebfa929b1
Revises: 62f6c2cd77a9
Create Date: 2024-05-30 13:41:26.572074

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '375ebfa929b1'
down_revision = '62f6c2cd77a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.String(length=25), nullable=True))
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.alter_column('address',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=120),
               existing_nullable=True)
        batch_op.alter_column('phone',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=True)
        batch_op.drop_column('price')

    # ### end Alembic commands ###