"""models

Revision ID: 9156bc805c3a
Revises: 
Create Date: 2023-11-17 08:45:41.494777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9156bc805c3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('director', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('budget', sa.Float(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('ongoing', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crew_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('production_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['production_id'], ['productions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crew_members')
    op.drop_table('productions')
    # ### end Alembic commands ###
