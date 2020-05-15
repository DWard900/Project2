"""exercise table

Revision ID: ea0ed8ed3527
Revises: 75f6c8bd0e2b
Create Date: 2020-05-14 14:50:42.277605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea0ed8ed3527'
down_revision = '75f6c8bd0e2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('style', sa.String(length=140), nullable=True),
    sa.Column('time', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_timestamp'), 'exercise', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exercise_timestamp'), table_name='exercise')
    op.drop_table('exercise')
    # ### end Alembic commands ###