# alembic/env.py
from __future__ import annotations

# ---------- PATH FIX: ensure 'backend/' is importable ----------
import os, sys
HERE = os.path.abspath(os.path.dirname(__file__))               # .../Tradex/alembic
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))   # .../Tradex
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")             # .../Tradex/backend

# Put backend/ first so 'core' and 'api' resolve (backend is their parent)
for p in (BACKEND_DIR, PROJECT_ROOT, HERE):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from backend.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------- Project imports ----------
# With BACKEND_DIR on sys.path, these work: 'core' and 'api' are under backend/
from backend.core.database import Base           # must define: Base = declarative_base()
from backend.api.models import user, task        # import ALL model modules that declare tables

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
