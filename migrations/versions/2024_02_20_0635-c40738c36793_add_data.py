"""'add_data'

Revision ID: c40738c36793
Revises: 4753bee1dd5b
Create Date: 2024-02-20 06:35:15.016558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy import text

from data.DataScanner import DataScanner

# revision identifiers, used by Alembic.
revision: str = 'c40738c36793'
down_revision: Union[str, None] = '4753bee1dd5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

data_scanner = DataScanner()


def upgrade() -> None:
    connection = op.get_bind()

    for item in data_scanner.get_files_data():
        table = sa.Table(item[0], sa.MetaData(), autoload_with=connection)  # type: ignore
        op.bulk_insert(table, item[1])  # type: ignore
        for i in range(len(item[1])):
            op.execute(text(f'''select setval('{table}_id_seq', (SELECT MAX(id) FROM {table}))'''))

    # ### end Alembic commands ###


def downgrade() -> None:
    for table in reversed(data_scanner.get_tables()):
        op.execute(f'TRUNCATE TABLE "{table}" CASCADE')
    # ### end Alembic commands ###
