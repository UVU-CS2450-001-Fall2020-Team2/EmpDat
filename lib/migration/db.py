from sqlalchemy import Table, MetaData, Column, BigInteger, String, Integer


def _migration_table(metadata=MetaData()):
    return Table('_migrations_', metadata,
                 Column('id', Integer, primary_key=True, sqlite_autoincrement=True),
                 Column('migration', String(255)),
                 Column('batch', Integer),
                 Column('applied_at', BigInteger),
                 extend_existing=True
                 )

