"""init

Revision ID: 0001
Revises: 
Create Date: 2023-01-01 00:00:00

"""

from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)
    op.create_index('ix_tasks_title', 'tasks', ['title'], unique=False)


def downgrade():
    op.drop_index('ix_tasks_title', table_name='tasks')
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')

