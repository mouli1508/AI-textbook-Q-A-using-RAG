class ChatHistoryManager:
    def __init__(self, db_manager, user_id, session_id):
        self.db_manager = db_manager
        self.user_id = user_id
        self.session_id = session_id
        self.chat_history = []

    def add_to_history(self, user_message, assistant_response, max_history_pairs):
        self.chat_history.append({"user": user_message})
        self.chat_history.append(
            {"assistant": assistant_response})

        if len(self.chat_history) > max_history_pairs * 2:
            self.chat_history = self.chat_history[-max_history_pairs * 2:]

        self.save_to_db(user_message, assistant_response)
        print("Chat history saved to database.")

    def save_to_db(self, user_message, assistant_response):
        if not self.user_id:
            print("Error: No user found in the database.")
            return
        query = """
            INSERT INTO chat_history (user_id, question, answer, session_id)
            VALUES (?, ?, ?, ?);
        """
        self.db_manager.execute_query(
            query, (self.user_id, user_message, assistant_response, self.session_id))

    def get_chat_history_for_summary(self):
        query = """
            SELECT question, answer FROM chat_history 
            WHERE session_id = ? ORDER BY timestamp ASC;
        """
        return self.db_manager.execute_query(query, (self.session_id,), fetch_all=True)

    def get_latest_summary(self):
        query = """
            SELECT summary_text FROM summary 
            WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1;
        """
        summary = self.db_manager.execute_query(
            query, (self.session_id,), fetch_one=True)
        return summary[0] if summary else None

    def save_summary_to_db(self, summary_text):

        if not self.user_id or not summary_text:
            return
        query = """
            INSERT INTO summary (user_id, session_id, summary_text)
            VALUES (?, ?, ?);
        """
        self.db_manager.execute_query(
            query, (self.user_id, self.session_id, summary_text))
        print("Summary saved to database.")

    def update_chat_summary(self, max_history_pairs, client, summary_model):
        chat_data = self.get_chat_history_for_summary()
        previous_summary = self.get_latest_summary()
        if len(chat_data) < max_history_pairs:
            return
        summary_text = self.generate_summary(
            client, summary_model, chat_data, previous_summary)
        if summary_text:
            self.save_summary_to_db(summary_text)

    def generate_summary(self, client, summary_model, chat_data, previous_summary):
        if not chat_data:
            return None
        summary_prompt = "Summarize the following conversation:\n\n"
        if previous_summary:
            summary_prompt += f"Previous summary:\n{previous_summary}\n\n"
        for q, a in chat_data:
            summary_prompt += f"User: {q}\nAssistant: {a}\n\n"
        summary_prompt += "Provide a concise summary while keeping important details."
        try:
            response = client.chat.completions.create(
                model=summary_model,
                messages=[{"role": "system", "content": summary_prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return None
