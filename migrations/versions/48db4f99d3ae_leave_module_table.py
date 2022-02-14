"""leave module table

Revision ID: 48db4f99d3ae
Revises: 5baee63e0dae
Create Date: 2022-02-07 06:16:12.571534

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '48db4f99d3ae'
down_revision = '5baee63e0dae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'leave_span', 
        sa.Column('id', UUID, primary_key=True),
        sa.Column('from_date', sa.Date, nullable=False),
        sa.Column('to_date', sa.Date, nullable=False),
        sa.Column('from_time', sa.String(25), nullable=False),
        sa.Column('to_time', sa.String(25), nullable=False),
    )
    
    op.create_table(
        'leave_type',
        sa.Column('id', UUID, primary_key=True),
        sa.Column('leave_type', sa.String(25), nullable=False),
    )

    op.create_table(
        'leave_allotment', 
        sa.Column('id', UUID, primary_key=True),
        sa.Column('employee_id', UUID, sa.ForeignKey('employees.employee_id')),
        sa.Column('alloted_leave', sa.Float(4,2), nullable=False),       
    )

    op.create_table(
        'leave_application',
        sa.Column('id', UUID, primary_key=True),
        sa.Column('leave_allotment_id',UUID,sa.ForeignKey('leave_allotment.id')),
        sa.Column('employee_id', UUID, sa.ForeignKey('employees.employee_id')),
        sa.Column('leave_span_id', UUID, sa.ForeignKey('leave_span.id')),
        sa.Column('leave_type_id', UUID, sa.ForeignKey('leave_type.id')),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('leave_days', sa.Float(4,2), nullable=False),
        sa.Column('leave_status',sa.String(25),nullable=False),
    )


def downgrade():
    op.drop_table('leave_application')
    op.drop_table('leave_allotment')
    op.drop_table('leave_type')
    op.drop_table('leave_span')
    
