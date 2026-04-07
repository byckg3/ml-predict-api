import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import ENV, postgre_settings
from app.db.relational.models import Base
from app.user.models import User


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option( "sqlalchemy.url", postgre_settings().async_db_url )

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
print( "Loaded tables:", target_metadata.tables.keys() )

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object( obj, name, type_, reflected, compare_to ):
    """
    Decides whether or not to include a database object in the autogenerate scan.

    :param obj: The database object being inspected ( e.g., Table, Column, or Index object ).
    :param name: The name of the object as a string ( e.g., "users" or "email" ).
    :param type_: The type of object, such as "table", "column", "index", or "foreign_key_constraint".
    :param reflected: Boolean. True if the object was found in the database ( reflected ), 
                      False if it exists only in the local SQLAlchemy models.
    :param compare_to: The counterpart object from the other side. 
                       - If reflected is True, this is the model's version of the object ( None if missing ).
                       - If reflected is False, this is the database's version of the object ( None if missing ).
    """
    
    # Check if the object being inspected is a Table
    if type_ == "table":
        
        # If the table exists in the database ( reflected = True), 
        # but is not defined in the SQLAlchemy models ( compare_to is None ),
        # return False to exclude it from the migration logic.
        # This prevents Alembic from generating 'op.drop_table()' operations.
        if reflected and compare_to is None:
            return False
    
    # For all other cases, return True to fallback to Alembic's default comparison behavior.
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object = include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure( 
        connection = connection, 
        target_metadata = target_metadata, 
        include_object = include_object
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
