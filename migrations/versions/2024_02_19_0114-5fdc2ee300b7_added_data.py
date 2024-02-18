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

from src.utils.PasswordUtils import get_hashed_password

# revision identifiers, used by Alembic.
revision: str = '5fdc2ee300b7'
down_revision: Union[str, None] = '394a529f5fe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    place_table = sa.Table('place', sa.MetaData(), autoload_with=connection)
    item_table = sa.Table('item', sa.MetaData(), autoload_with=connection)
    user_table = sa.Table('user', sa.MetaData(), autoload_with=connection)

    op.bulk_insert(place_table, [
        {"name": "Стол в 201", "max_weight": 20},
        {"name": "Подоконник в коридоре", "max_weight": 10},
        {"name": "Полка у шкафа в 110", "max_weight": 15},
    ])

    op.bulk_insert(item_table, [
        {"name": "Пачка чая", "weight": 5, "place_id": 1},
        {"name": "Коробка печенья", "weight": 10, "place_id": 2},
        {"name": "Банка кофе", "weight": 3, "place_id": 3},
    ])

    op.bulk_insert(user_table, [
        {"username": "user1", "hashed_password": get_hashed_password('Pa$$w0rd')},  # 4 test only
        {"username": "user2", "hashed_password": get_hashed_password('Pa$$w0rd')},  # 4 test only
    ])

    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("DELETE FROM item WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM place WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM user WHERE id IN (1, 2)")
    # ### end Alembic commands ###
