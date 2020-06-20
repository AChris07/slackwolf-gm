"""add_game_user_role

Revision ID: 4c1f0c640ee4
Revises: 9c79444045d7
Create Date: 2020-07-04 14:35:37.218274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c1f0c640ee4'
down_revision = '9c79444045d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('game_user',
                  sa.Column('role',
                            sa.Enum('VILLAGER',
                                    'WEREWOLF',
                                    'SEER',
                                    name='roletypes'),
                            nullable=False)
                  )


def downgrade():
    op.drop_column('game_user', 'role')
