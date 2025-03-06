class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_info = self.get_user_info()
        self.user_id = self.get_user_id()

    def get_user_info(self):
        query = "SELECT * FROM user_info LIMIT 1;"
        user = self.db_manager.execute_query(query, fetch_one=True)
        if user:
            return {
                "id": user[0],
                "name": user[1],
                "last_name": user[2],
                "occupation": user[3],
                "country": user[4],
            }
        return None

    def get_user_id(self):
        query = "SELECT id FROM user_info LIMIT 1;"
        user = self.db_manager.execute_query(query, fetch_one=True)
        return user[0] if user else None
