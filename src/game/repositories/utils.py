from sqlite3 import Cursor


def create_table(cursor: Cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id SMALLINT NOT NULL UNIQUE,
            jwt CHARACTER(128) NOT NULL UNIQUE
        )
    """,
    )
