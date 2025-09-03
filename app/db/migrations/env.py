# app/db/migrations/env.py
from __future__ import annotations

# --- Make project root importable for Alembic ---
# Alembic runs from the migrations folder, so Python can't find top-level "app".
# We add "/app" (the project root in the container) to sys.path explicitly.
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # /app
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# ------------------------------------------------

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.models import Base

# Alembic config object, provides access to values within the .ini file.
config = context.config

# Prefer URL from settings (env var), fallback to alembic.ini default.
if settings.database_url:
    config.set_main_option("sqlalchemy.url", settings.database_url)
else:
    config.set_main_option(
        "sqlalchemy.url",
        config.get_main_option(
            "sqlalchemy.url",
            "postgresql+psycopg://postgres:postgres@db:5432/celery_app",
        ),
    )

# Enable Alembic logging if config file is present.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata used by autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate SQL scripts without a DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a real DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()