"""function and trigger

Revision ID: bda96c0c2257
Revises: 7a52aeb252b8
Create Date: 2024-08-18 12:41:17.897439

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bda96c0c2257'
down_revision: Union[str, None] = '7a52aeb252b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Создание функции и триггера для управления балансом."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_user_balance()
        RETURNS TRIGGER AS $$
        BEGIN

        IF TG_OP = 'INSERT' THEN
            IF NEW.transaction_type = 'credit' THEN
                UPDATE "user"
                SET balance = balance + NEW.amount
                WHERE id = NEW.user_id;
            ELSIF NEW.transaction_type = 'debit' THEN
                UPDATE "user"
                SET balance = balance - NEW.amount
                WHERE id = NEW.user_id;
            END IF;
        END IF;

        IF TG_OP = 'UPDATE' THEN
            -- Если изменилось поле amount
            IF NEW.transaction_type = OLD.transaction_type THEN
                IF NEW.transaction_type = 'credit' THEN
                    UPDATE "user"
                    SET balance = balance - OLD.amount + NEW.amount
                    WHERE id = NEW.user_id;
                ELSIF NEW.transaction_type = 'debit' THEN
                    UPDATE "user"
                    SET balance = balance + OLD.amount - NEW.amount
                    WHERE id = NEW.user_id;
                END IF;
            ELSE

                IF OLD.transaction_type = 'credit' THEN
                    UPDATE "user"
                    SET balance = balance - OLD.amount
                    WHERE id = OLD.user_id;
                ELSIF OLD.transaction_type = 'debit' THEN
                    UPDATE "user"
                    SET balance = balance + OLD.amount
                    WHERE id = OLD.user_id;
                END IF;

                IF NEW.transaction_type = 'credit' THEN
                    UPDATE "user"
                    SET balance = balance + NEW.amount
                    WHERE id = NEW.user_id;
                ELSIF NEW.transaction_type = 'debit' THEN
                    UPDATE "user"
                    SET balance = balance - NEW.amount
                    WHERE id = NEW.user_id;
                END IF;
            END IF;
        END IF;

        IF TG_OP = 'DELETE' THEN
            IF OLD.transaction_type = 'credit' THEN
                UPDATE "user"
                SET balance = balance - OLD.amount
                WHERE id = OLD.user_id;
            ELSIF OLD.transaction_type = 'debit' THEN
                UPDATE "user"
                SET balance = balance + OLD.amount
                WHERE id = OLD.user_id;
            END IF;
        END IF;

        RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """,
    )
    op.execute(
        """
        CREATE TRIGGER trigger_update_balance
        AFTER INSERT OR UPDATE OR DELETE ON "transaction"
        FOR EACH ROW
        EXECUTE FUNCTION update_user_balance();
        """,
    )


def downgrade() -> None:
    """Дроп функции и триггера для управления балансом."""
    op.execute(
        """
        DROP FUNCTION IF EXISTS update_user_balance();
        """,
    )
    op.execute(
        """
        DROP TRIGGER IF EXISTS trigger_update_balance ON "transaction";
        """,
    )
