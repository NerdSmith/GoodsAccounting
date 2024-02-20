"""added data

Revision ID: 5fdc2ee300b7
Revises: 394a529f5fe7
Create Date: 2024-02-19 01:14:11.122978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy import MetaData, Table, insert
from sqlalchemy.util.preloaded import orm

from data.DataScanner import DataScanner
from src.utils.PasswordUtils import get_hashed_password

# revision identifiers, used by Alembic.
revision: str = '5fdc2ee300b7'
down_revision: Union[str, None] = '394a529f5fe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

data_scanner = DataScanner()


def upgrade() -> None:
    connection = op.get_bind()

    for item in data_scanner.get_files_data():
        table = sa.Table(item[0], sa.MetaData(), autoload_with=connection)  # type: ignore
        op.bulk_insert(table, item[1])  # type: ignore

    # ### end Alembic commands ###


def downgrade() -> None:
    for table in reversed(data_scanner.get_tables()):
        op.execute(f'TRUNCATE TABLE "{table}" CASCADE')
    # ### end Alembic commands ###
