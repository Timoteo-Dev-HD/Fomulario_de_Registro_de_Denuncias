import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Permite importar o app e o db
sys.path.append(os.getcwd())

# importa o db e o app Flask
from src.settings.extensions import db
from app import app

# Config do Alembic (alembic.ini)
config = context.config

# Logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados que o Alembic vai monitorar
target_metadata = db.metadata


def run_migrations_offline():
    """
    Executa migrations sem conexão real (gera SQL).
    Usado raramente — CI/CD, scripts, etc.
    """
    url = app.config["SQLALCHEMY_DATABASE_URI"]
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Executa migrations com conexão real ao banco
    (uso normal)
    """
    # garante contexto do Flask para acessar config
    with app.app_context():
        configuration = config.get_section(config.config_ini_section)
        configuration["sqlalchemy.url"] = app.config["SQLALCHEMY_DATABASE_URI"]

        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()


# Seleciona modo (online/offline)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
