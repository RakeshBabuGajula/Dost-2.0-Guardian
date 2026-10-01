"""Initial application foundation schema migration

Revision ID: 001_initial_schema

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. Teams
    op.create_table(
        'teams',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('supervisor_id', sa.String(length=36), nullable=True),
        sa.Column('assigned_section', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['supervisor_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_code'), 'teams', ['code'], unique=True)

    # 3. Block Sections
    op.create_table(
        'block_sections',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('line_type', sa.String(length=50), nullable=False),
        sa.Column('start_km', sa.Float(), nullable=False),
        sa.Column('end_km', sa.Float(), nullable=False),
        sa.Column('speed_limit_kmh', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_block_sections_code'), 'block_sections', ['code'], unique=True)

    # 4. Workers
    op.create_table(
        'workers',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=False),
        sa.Column('team_id', sa.String(length=36), nullable=True),
        sa.Column('current_block_section', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('network_state', sa.String(length=20), nullable=False),
        sa.Column('battery_level', sa.Integer(), nullable=False),
        sa.Column('gps_accuracy_meters', sa.Float(), nullable=False),
        sa.Column('position_x', sa.Float(), nullable=False),
        sa.Column('position_y', sa.Float(), nullable=False),
        sa.Column('unacknowledged_alert_id', sa.String(length=50), nullable=True),
        sa.Column('envelope_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. Trains
    op.create_table(
        'trains',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('number', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('line', sa.String(length=50), nullable=False),
        sa.Column('current_block_section', sa.String(length=100), nullable=False),
        sa.Column('position_x', sa.Float(), nullable=False),
        sa.Column('speed_kmh', sa.Float(), nullable=False),
        sa.Column('direction', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. Work Zones
    op.create_table(
        'work_zones',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('block_section_code', sa.String(length=100), nullable=False),
        sa.Column('start_x', sa.Float(), nullable=False),
        sa.Column('end_x', sa.Float(), nullable=False),
        sa.Column('buffer_zone_meters', sa.Float(), nullable=False),
        sa.Column('safety_zone_meters', sa.Float(), nullable=False),
        sa.Column('assigned_team_code', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. Alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('worker_id', sa.String(length=50), nullable=False),
        sa.Column('worker_name', sa.String(length=255), nullable=False),
        sa.Column('train_id', sa.String(length=50), nullable=False),
        sa.Column('train_name', sa.String(length=255), nullable=False),
        sa.Column('block_section_code', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('time_to_danger_seconds', sa.Integer(), nullable=False),
        sa.Column('distance_to_train_meters', sa.Float(), nullable=False),
        sa.Column('escalation_tier', sa.String(length=50), nullable=False),
        sa.Column('required_action', sa.Text(), nullable=False),
        sa.Column('is_acknowledged', sa.Boolean(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
        sa.Column('acknowledged_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 8. Near Misses
    op.create_table(
        'near_misses',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('occurred_at', sa.DateTime(), nullable=False),
        sa.Column('train_id', sa.String(length=50), nullable=False),
        sa.Column('train_speed_kmh', sa.Float(), nullable=False),
        sa.Column('worker_id', sa.String(length=50), nullable=False),
        sa.Column('worker_name', sa.String(length=255), nullable=False),
        sa.Column('block_section_code', sa.String(length=100), nullable=False),
        sa.Column('min_spatial_clearance_meters', sa.Float(), nullable=False),
        sa.Column('ttd_at_ack_seconds', sa.Integer(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False),
        sa.Column('contributing_factors', sa.JSON(), nullable=False),
        sa.Column('location_coords', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 9. Emergency Events
    op.create_table(
        'emergency_events',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('event_id', sa.String(length=100), nullable=False),
        sa.Column('worker_id', sa.String(length=50), nullable=False),
        sa.Column('block_section_code', sa.String(length=100), nullable=False),
        sa.Column('trigger_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('acknowledged_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id')
    )

    # 10. Devices
    op.create_table(
        'devices',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('worker_id', sa.String(length=50), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=False),
        sa.Column('firmware_version', sa.String(length=50), nullable=False),
        sa.Column('battery_percentage', sa.Integer(), nullable=False),
        sa.Column('network_signal_dbm', sa.Integer(), nullable=False),
        sa.Column('last_ping_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 11. Audit Logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('event_id', sa.String(length=100), nullable=False),
        sa.Column('actor', sa.String(length=255), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('target', sa.String(length=255), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('request_id', sa.String(length=100), nullable=True),
        sa.Column('correlation_id', sa.String(length=100), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id')
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('devices')
    op.drop_table('emergency_events')
    op.drop_table('near_misses')
    op.drop_table('alerts')
    op.drop_table('work_zones')
    op.drop_table('trains')
    op.drop_table('workers')
    op.drop_table('block_sections')
    op.drop_table('teams')
    op.drop_table('users')
