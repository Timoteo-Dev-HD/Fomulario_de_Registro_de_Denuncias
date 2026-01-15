from alembic import op
import sqlalchemy as sa

revision = "8b62ead9efc2"
down_revision = "ca60cadce63f"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ cria a coluna (nullable no início)
    with op.batch_alter_table("denuncias") as batch_op:
        batch_op.add_column(
            sa.Column("data_public", sa.Date(), nullable=True)
        )

    # 2️⃣ preenche registros antigos
    op.execute(
        "UPDATE denuncias SET data_public = CURDATE() WHERE data_public IS NULL"
    )

    # 3️⃣ agora sim pode tornar NOT NULL
    with op.batch_alter_table("denuncias") as batch_op:
        batch_op.alter_column(
            "data_public",
            existing_type=sa.Date(),
            nullable=False
        )


def downgrade():
    with op.batch_alter_table("denuncias") as batch_op:
        batch_op.drop_column("data_public")
