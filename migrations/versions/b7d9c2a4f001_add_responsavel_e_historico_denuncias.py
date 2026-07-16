"""Add responsavel e historico de denuncias.

Revision ID: b7d9c2a4f001
Revises: aae95a3bc222
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7d9c2a4f001"
down_revision: Union[str, Sequence[str], None] = "aae95a3bc222"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("denuncias", sa.Column("responsavel", sa.String(length=150), nullable=True))
    op.create_table(
        "denuncias_historico",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("denuncia_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("campo", sa.String(length=80), nullable=False),
        sa.Column("valor_anterior", sa.Text(), nullable=True),
        sa.Column("valor_novo", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["denuncia_id"], ["denuncias.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("denuncias_historico")
    op.drop_column("denuncias", "responsavel")
