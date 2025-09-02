from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.db.models import Base

# 1) settings and models
from app.core.config import settings
from app.db.models import Base

# 2) basic alembic configuration
config = context.config

# 3) config url from Settings (.env)
if settings.database_url:
    config.set_main_option("sqlalchemy.url", settings.database_url)

# 4) alembic logging
# if config.config_file_name is not None:
#    fileConfig(config.config_file_name)

# 5) metadata for autogenertaion
target_metadata = Base.metadata

def run_migrations_offline():
    """Migrations not truly connected to DB in offline"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Migrations connected to DB in online regimen"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()