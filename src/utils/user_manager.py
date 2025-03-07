import math
from typing import Optional, Dict, Any
from utils.database_manager import DatabaseManager


class UserManager:
    """
    Manages user-related operations, including retrieving user information and user ID
    from the database.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initializes the UserManager with a database manager.

        Args:
            db_manager (DatabaseManager): The database manager instance to execute queries.
        """
        self.db_manager = db_manager
        self.user_info = self.get_user_info()
        self.user_id = self.get_user_id()

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves user information from the database, filtering out empty values, None, and NaN.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing user information with valid values,
            or None if no user is found.
        """
        query = "SELECT * FROM user_info LIMIT 1;"
        user = self.db_manager.execute_query(query, fetch_one=True)
        if user:
            user_info = {
                "id": user[0],
                "name": user[1],
                "last_name": user[2],
                "occupation": user[3],
                "location": user[4],
                "gender": user[5],
                "age": user[6],
                "interests": user[7]
            }
            return {k: v for k, v in user_info.items() if v not in (None, "") and not (isinstance(v, float) and math.isnan(v))}
        return None

    def get_user_id(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the user ID from the database.

        Returns:
            Optional[int]: The user ID if found, otherwise None.
        """
        query = "SELECT id FROM user_info LIMIT 1;"
        user = self.db_manager.execute_query(query, fetch_one=True)
        return user[0] if user else None
