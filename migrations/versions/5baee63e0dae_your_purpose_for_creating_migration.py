"""your purpose for creating migration

Revision ID: 5baee63e0dae
Revises: 
Create Date: 2021-12-18 12:10:59.737703

"""
from alembic import op
import sqlalchemy as sa
from  sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '5baee63e0dae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'countries', 
        sa.Column('country_id', UUID,primary_key=True),
        sa.Column('country_name', sa.String(255)),
    )

    op.create_table(
        'employees',
        sa.Column('employee_id', UUID, primary_key=True),
        sa.Column('country_id', UUID, sa.ForeignKey('countries.country_id')),
        sa.Column('employee_code', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('employee_role', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phno', sa.String(25), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('gender', sa.String(255), nullable=False),
        sa.Column('otp', sa.String(25))
    )


def downgrade():
    op.drop_table('employees')
    op.drop_table('countries')
