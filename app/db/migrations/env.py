# ruff: noqa: E402  # English: allow imports after sys.path manipulation

from __future__ import annotations

# English: put project root on sys.path so `app.*` imports work when Alembic runs standalone
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # /app
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------- third-party & local imports (after sys.path tweak) ----------------
from logging.config import fileConfig  # English: stdlib

from alembic import context  # English: third-party
from sqlalchemy import engine_from_config, pool

from app.core.config import settings  # English: local
from app.db.models import Base

# ... (далі без змін)

# English: Alembic config object; values are read from alembic.ini unless overridden below
config = context.config

# English: prefer URL from Settings (env var) over alembic.ini default
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

# English: enable Alembic logging if config file is present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# English: metadata used by autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Генерація SQL без підключення до БД."""
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
    """Запуск міграцій з підключенням до БД."""
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
