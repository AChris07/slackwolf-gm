from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context

import sys
import os
sys.path.insert(0, os.getcwd())
from slackwolf.db import Base # noqa E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_flask_inst_config():
    """Accesses the current flask instance config file, if available"""
    try:
        with open('instance/config.cfg') as file:
            config = dict()
            for line in file:
                key, val = line.split('=')
                config[key] = val.strip().strip("\'").strip('\"')

            return config
    except FileNotFoundError:
        return dict()


def get_url():
    """Returns the DB URL set up for the project"""
    try:
        return get_flask_inst_config()['DATABASE_URL']
    except KeyError:
        raise ValueError("Database URL is not set")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_url()
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
