"""create_initial_schema

Revision ID: 9c79444045d7
Revises:
Create Date: 2020-05-17 13:00:45.335361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c79444045d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('team',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('slack_id', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('slack_id'))

    op.create_table('channel',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('slack_id', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('team_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('team_id', 'slack_id'))

    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('slack_id', sa.String(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('team_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('team_id', 'slack_id'))

    op.create_table('game',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('status',
                              sa.Enum('WAITING',
                                      'STARTED',
                                      'FINISHED',
                                      name='gamestatus'),
                              nullable=False),
                    sa.Column('channel_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('game_user',
                    sa.Column('game_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('game_id', 'user_id'))


def downgrade():
    op.drop_table('game_user')
    op.drop_table('game')
    op.drop_table('user')
    op.drop_table('channel')
    op.drop_table('team')
