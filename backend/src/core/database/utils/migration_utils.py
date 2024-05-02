from alembic import op
from sqlalchemy import Enum, MetaData, text

from src.core.enums import BaseEnum


def enum_exists(enum_name: str) -> bool:
    conn = op.get_bind()
    query_string = f"""SELECT count(*) FROM pg_type WHERE typcategory = 'E' and typname = '{enum_name}'; """
    result = conn.execute(text(query_string))
    return result.first()[0] == 1


def get_enum(name: str, enum_cls: type[BaseEnum]):
    if not enum_exists(name):
        db_enum = Enum(*enum_cls.values(), name=name)
    else:
        metadata = MetaData()
        metadata.bind = op.get_bind()
        db_enum = Enum(name=name, metadata=metadata, create_type=False)
    return db_enum


def drop_enum(enum_name: str) -> bool:
    if enum_exists(enum_name):
        conn = op.get_bind()
        query_string = f"""DROP TYPE {enum_name}"""
        conn.execute(text(query_string))

    return True
