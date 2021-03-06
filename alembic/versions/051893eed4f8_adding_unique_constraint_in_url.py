"""Adding unique constraint in URL

Revision ID: 051893eed4f8
Revises: 
Create Date: 2021-12-06 09:19:56.433572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '051893eed4f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_key')
    op.create_unique_constraint(None, 'video', ['url'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'video', type_='unique')
    op.create_table('api_key',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('key', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('quota_exhausted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='api_key_pkey')
    )
    # ### end Alembic commands ###
