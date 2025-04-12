import math
from typing import Optional, Dict, Any
from utils.sql_manager import SQLManager


class UserManager:
    """
    Manages user-related operations, including retrieving user information and user ID
    from the database.
    """

    def __init__(self, sql_manager: SQLManager):
        """
        Initializes the UserManager with a database manager.

        Args:
            sql_manager (SQLManager): The database manager instance to execute queries.
        """
        self.sql_manager = sql_manager
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
        user = self.sql_manager.execute_query(query, fetch_one=True)
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
        user = self.sql_manager.execute_query(query, fetch_one=True)
        return user[0] if user else None

    def add_user_info_to_database(self, **kwargs: dict) -> str:
        """
        Updates the user information in the database if valid keys are provided.
        Merges interests instead of overwriting them.

        Args:
            user_info (dict): Dictionary containing user attributes to update.

        Returns:
            bool: True if the update was successful, False if invalid keys are provided.
        """
        try:
            valid_keys = {"name", "last_name", "age", "gender",
                          "location", "occupation", "interests"}

            for key in kwargs.keys():
                if key not in valid_keys:
                    return "Function call failed.", "Please provide a valid key from the following list: name, last_name, age, gender, location, occupation, interests"

            # Convert interests list to comma-separated string if provided
            if "interests" in kwargs and isinstance(kwargs["interests"], list):
                # Step 1: Fetch current interests from DB
                query = "SELECT interests FROM user_info LIMIT 1;"
                result = self.sql_manager.fetch_one(query)

                existing_interests = []
                if result and result[0]:
                    existing_interests = [
                        i.strip() for i in result[0].split(",") if i.strip()]

                 # Step 2: Convert new interests to set
                new_interests = [i.strip()
                                 for i in kwargs["interests"] if isinstance(i, str)]

                # Step 3: Merge and remove duplicates
                merged_interests = sorted(
                    set(existing_interests + new_interests))

                # Step 4: Convert back to comma-separated string
                kwargs["interests"] = ", ".join(merged_interests)

            # Prepare the SET clause
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            params = tuple(kwargs.values())

            query = f"""
            UPDATE user_info
            SET {set_clause}
            WHERE id = (SELECT id FROM user_info LIMIT 1);
            """

            self.sql_manager.execute_query(query, params)
            return "Function call successful.", "User information updated."
        except Exception as e:
            return "Function call failed.", f"Error: {e}"
