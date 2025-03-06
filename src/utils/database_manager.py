import sqlite3
from pyprojroot import here


class DatabaseManager:
    def __init__(self, db_path=here("data/chatbot.db")):
        self.db_path = db_path

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False) -> list:
        """
        Executes an SQL query with optional parameters and fetch options.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass to the SQL query. Defaults to ().
            fetch_one (bool, optional): Whether to fetch a single row. Defaults to False.
            fetch_all (bool, optional): Whether to fetch all rows. Defaults to False.

        Returns:
            list: Query results if fetching is enabled; otherwise, None.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone() if fetch_one else cursor.fetchall() if fetch_all else None
        conn.commit()
        conn.close()
        return result
