"""empty message

Revision ID: 583b6dd88b5f
Revises: 3a4227a54cfa
Create Date: 2017-01-12 13:23:18.079632

"""

# revision identifiers, used by Alembic.
revision = '583b6dd88b5f'
down_revision = '3a4227a54cfa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_todo_list_description', table_name='todo_list')
    op.create_index(op.f('ix_todo_list_description'), 'todo_list', ['description'], unique=False)
    op.drop_index('ix_todo_list_status', table_name='todo_list')
    op.create_index(op.f('ix_todo_list_status'), 'todo_list', ['status'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todo_list_status'), table_name='todo_list')
    op.create_index('ix_todo_list_status', 'todo_list', ['status'], unique=1)
    op.drop_index(op.f('ix_todo_list_description'), table_name='todo_list')
    op.create_index('ix_todo_list_description', 'todo_list', ['description'], unique=1)
    ### end Alembic commands ###