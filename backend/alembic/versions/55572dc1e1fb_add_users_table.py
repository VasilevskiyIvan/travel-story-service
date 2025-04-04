"""Add users table

Revision ID: 55572dc1e1fb
Revises: 08dece376c5d
Create Date: 2025-03-19 23:32:12.552842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '55572dc1e1fb'
down_revision: Union[str, None] = '08dece376c5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('icon_path', sa.Text(), nullable=True),
    sa.Column('earned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_user_id'), 'achievements', ['user_id'], unique=False)
    op.create_table('subscriptions',
    sa.Column('follower_id', sa.UUID(), nullable=False),
    sa.Column('following_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'following_id')
    )
    op.create_index('idx_subscriptions_follower', 'subscriptions', ['follower_id'], unique=False)
    op.create_index('idx_subscriptions_following', 'subscriptions', ['following_id'], unique=False)
    op.create_table('travel_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('location', sa.Text(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('visited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_latitude'),
    sa.CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_longitude'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coordinates', 'travel_map', ['latitude', 'longitude'], unique=False)
    op.create_index(op.f('ix_travel_map_user_id'), 'travel_map', ['user_id'], unique=False)
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('report_card_id', sa.Integer(), nullable=False),
    sa.Column('destination', sa.String(length=255), nullable=False),
    sa.Column('main_image', sa.String(length=512), nullable=True),
    sa.Column('html_path', sa.Text(), nullable=False),
    sa.Column('text_content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('status', sa.Enum('draft', 'private', 'public', 'friends_only', name='report_status', create_constraint=True), nullable=True),
    sa.ForeignKeyConstraint(['report_card_id'], ['report_card_content.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('report_card_id')
    )
    op.create_index('idx_report_status', 'reports', ['status'], unique=False)
    op.create_index('ix_report_text_content', 'reports', [sa.literal_column("to_tsvector('english', text_content)")], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_reports_user_id'), 'reports', ['user_id'], unique=False)
    op.create_table('additional_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('file_type', sa.Enum('image', 'document', 'other', name='additional_file_type', create_constraint=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_additional_files_report_id'), 'additional_files', ['report_id'], unique=False)
    op.create_table('collaborators',
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role', sa.Enum('editor', 'viewer', name='collaborator_role', create_constraint=True), nullable=False),
    sa.Column('added_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('report_id', 'user_id')
    )
    op.create_table('media_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('file_type', sa.Enum('image', 'video', 'audio', 'document', name='media_file_type', create_constraint=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('file_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('file_hash', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_files_report_id'), 'media_files', ['report_id'], unique=False)
    op.add_column('report_card_content', sa.Column('user_id', sa.UUID(), nullable=False))
    op.add_column('report_card_content', sa.Column('likes', sa.Integer(), nullable=False))
    op.add_column('report_card_content', sa.Column('comments_count', sa.Integer(), nullable=False))
    op.alter_column('report_card_content', 'status',
               existing_type=postgresql.ENUM('PRIVATE', 'SUBSCRIBERS', 'PUBLIC', name='reportstatusenum'),
               type_=sa.Enum('draft', 'private', 'public', 'friends_only', name='report_status', create_constraint=True),
               existing_nullable=True)
    op.create_index('idx_report_card_status', 'report_card_content', ['status'], unique=False)
    op.create_index('idx_report_card_user', 'report_card_content', ['user_id'], unique=False)
    op.create_index(op.f('ix_report_card_content_user_id'), 'report_card_content', ['user_id'], unique=False)
    op.create_foreign_key(None, 'report_card_content', 'users', ['user_id'], ['user_id'])
    op.drop_column('report_card_content', 'created_at')
    op.drop_column('report_card_content', 'changed_at')
    op.create_index('idx_user_report_card', 'user_report_card', ['user_id', 'report_id'], unique=False)
    op.add_column('users', sa.Column('profile_visibility', sa.Enum('public', 'private', 'friends_only', name='profile_visibility', create_constraint=True), nullable=True))
    op.add_column('users', sa.Column('travel_stats', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('USER', 'ADMIN', 'MODERATOR', name='roleenum'),
               type_=sa.Enum('user', 'admin', 'moderator', name='user_role', create_constraint=True),
               existing_nullable=True)
    op.alter_column('users', 'account_status',
               existing_type=postgresql.ENUM('ACTIVE', 'SUSPENDED', 'DELETED', name='accountstatusenum'),
               type_=sa.Enum('active', 'suspended', 'deleted', name='account_status', create_constraint=True),
               existing_nullable=True)
    op.alter_column('users', 'preferences',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)
    op.create_index('idx_user_email', 'users', ['email'], unique=False)
    op.create_index('idx_user_username', 'users', ['username'], unique=False)
    op.create_index('ix_user_travel_stats', 'users', ['travel_stats'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_travel_stats', table_name='users', postgresql_using='gin')
    op.drop_index('idx_user_username', table_name='users')
    op.drop_index('idx_user_email', table_name='users')
    op.alter_column('users', 'preferences',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)
    op.alter_column('users', 'account_status',
               existing_type=sa.Enum('active', 'suspended', 'deleted', name='account_status', create_constraint=True),
               type_=postgresql.ENUM('ACTIVE', 'SUSPENDED', 'DELETED', name='accountstatusenum'),
               existing_nullable=True)
    op.alter_column('users', 'role',
               existing_type=sa.Enum('user', 'admin', 'moderator', name='user_role', create_constraint=True),
               type_=postgresql.ENUM('USER', 'ADMIN', 'MODERATOR', name='roleenum'),
               existing_nullable=True)
    op.drop_column('users', 'travel_stats')
    op.drop_column('users', 'profile_visibility')
    op.drop_index('idx_user_report_card', table_name='user_report_card')
    op.add_column('report_card_content', sa.Column('changed_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('report_card_content', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'report_card_content', type_='foreignkey')
    op.drop_index(op.f('ix_report_card_content_user_id'), table_name='report_card_content')
    op.drop_index('idx_report_card_user', table_name='report_card_content')
    op.drop_index('idx_report_card_status', table_name='report_card_content')
    op.alter_column('report_card_content', 'status',
               existing_type=sa.Enum('draft', 'private', 'public', 'friends_only', name='report_status', create_constraint=True),
               type_=postgresql.ENUM('PRIVATE', 'SUBSCRIBERS', 'PUBLIC', name='reportstatusenum'),
               existing_nullable=True)
    op.drop_column('report_card_content', 'comments_count')
    op.drop_column('report_card_content', 'likes')
    op.drop_column('report_card_content', 'user_id')
    op.drop_index(op.f('ix_media_files_report_id'), table_name='media_files')
    op.drop_table('media_files')
    op.drop_table('collaborators')
    op.drop_index(op.f('ix_additional_files_report_id'), table_name='additional_files')
    op.drop_table('additional_files')
    op.drop_index(op.f('ix_reports_user_id'), table_name='reports')
    op.drop_index('ix_report_text_content', table_name='reports', postgresql_using='gin')
    op.drop_index('idx_report_status', table_name='reports')
    op.drop_table('reports')
    op.drop_index(op.f('ix_travel_map_user_id'), table_name='travel_map')
    op.drop_index('idx_coordinates', table_name='travel_map')
    op.drop_table('travel_map')
    op.drop_index('idx_subscriptions_following', table_name='subscriptions')
    op.drop_index('idx_subscriptions_follower', table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_achievements_user_id'), table_name='achievements')
    op.drop_table('achievements')
    # ### end Alembic commands ###
