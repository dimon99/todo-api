"""empty message

Revision ID: 65528cdd4bf7
Revises: 583b6dd88b5f
Create Date: 2017-01-12 13:29:30.798821

"""

# revision identifiers, used by Alembic.
revision = '65528cdd4bf7'
down_revision = '583b6dd88b5f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_todo_list_uri', table_name='todo_list')
    op.create_index(op.f('ix_todo_list_uri'), 'todo_list', ['uri'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todo_list_uri'), table_name='todo_list')
    op.create_index('ix_todo_list_uri', 'todo_list', ['uri'], unique=1)
    ### end Alembic commands ###
