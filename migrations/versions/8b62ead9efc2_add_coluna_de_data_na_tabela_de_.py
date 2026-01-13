from alembic import op
import sqlalchemy as sa

revision = "8b62ead9efc2"
down_revision = "ca60cadce63f"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ garantir que não existam NULLs
    op.execute(
        "UPDATE denuncias SET data_public = CURDATE() WHERE data_public IS NULL"
    )

    # 2️⃣ agora sim pode virar NOT NULL (MySQL exige existing_type)
    with op.batch_alter_table("denuncias") as batch_op:
        batch_op.alter_column(
            "data_public",
            existing_type=sa.Date(),
            nullable=False
        )


def downgrade():
    with op.batch_alter_table("denuncias") as batch_op:
        batch_op.alter_column(
            "data_public",
            existing_type=sa.Date(),
            nullable=True
        )
