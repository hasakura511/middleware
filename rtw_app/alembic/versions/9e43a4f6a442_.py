"""

Revision ID: 9e43a4f6a442
Revises: bbbee32513d1
Create Date: 2021-11-02 10:08:56.387807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e43a4f6a442'
down_revision = 'bbbee32513d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('img_url_type', sa.String(), nullable=True),
    sa.Column('caption', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
