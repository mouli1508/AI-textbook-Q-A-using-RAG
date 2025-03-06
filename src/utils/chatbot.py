import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from utils.database_manager import DatabaseManager
from utils.user_manager import UserManager
from utils.chat_history_manager import ChatHistoryManager
from utils.prepare_prompt import prepare_system_prompt
# Load environment variables
load_dotenv()


class Chatbot:
    def __init__(self,
                 chat_model: str = "gpt-4o-mini",
                 summary_model: str = "gpt-3.5-turbo",
                 max_history_pairs: int = 2):

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat_model = chat_model
        self.summary_model = summary_model
        self.max_history_pairs = max_history_pairs

        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.session_id = str(uuid.uuid4())

        self.chat_history_manager = ChatHistoryManager(
            self.db_manager, self.user_manager.user_id, self.session_id)
        self.previous_summary = self.chat_history_manager.get_latest_summary()

    def chat(self, user_message):
        system_prompt = prepare_system_prompt(self.user_manager.user_info,
                                              self.previous_summary,
                                              self.chat_history_manager.chat_history)
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_message}]
            )
            assistant_response = response.choices[0].message.content
            self.chat_history_manager.add_to_history(
                user_message, assistant_response, self.max_history_pairs)
            self.chat_history_manager.update_chat_summary(
                self.max_history_pairs, self.client, self.summary_model)
            return assistant_response
        except Exception as e:
            return f"Error: {str(e)}"
