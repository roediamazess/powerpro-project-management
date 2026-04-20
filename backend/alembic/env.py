import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Core app imports
from app.core.config import settings
from app.db.base import Base
# Import all models here for metadata discovery
from app.models.auth import User, Role, Tier
from app.models.partner import Partner, PartnerContact, PartnerType, PartnerStatus
from app.models.project import Project, ProjectPIC, ProjectType, ProjectStatus
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.compliance import ComplianceForm, ComplianceItem, ComplianceEntry, ComplianceEntryScore
from app.models.audit import SystemAuditLog

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    config_section = config.get_section(config.config_ini_section)
    config_section["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = async_engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
