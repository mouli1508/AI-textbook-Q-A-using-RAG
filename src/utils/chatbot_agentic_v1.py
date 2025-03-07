import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from utils.database_manager import DatabaseManager
from utils.user_manager import UserManager
from utils.chat_history_manager import ChatHistoryManager
from utils.search_manager import SearchManager
from utils.prepare_prompt import prepare_system_prompt_for_agentic_chatbot_v1
from utils.utils import Utils
from utils.config import Config
from traceback import format_exc
import json

load_dotenv()


class Chatbot:
    def __init__(self):

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cfg = Config()
        self.chat_model = self.cfg.chat_model
        self.summary_model = self.cfg.summary_model
        self.temperature = self.cfg.temperature
        self.max_history_pairs = self.cfg.max_history_pairs

        self.session_id = str(uuid.uuid4())
        self.utils = Utils()
        self.db_manager = DatabaseManager(self.cfg.db_path)
        self.user_manager = UserManager(self.db_manager)
        self.chat_history_manager = ChatHistoryManager(
            self.db_manager, self.user_manager.user_id, self.session_id)
        self.previous_summary = self.chat_history_manager.get_latest_summary()

        self.search_manager = SearchManager(
            self.db_manager, self.utils, self.client, self.summary_model, self.cfg.max_characters)
        self.agent_functions = [self.utils.jsonschema(self.chat_history_manager.add_user_info_to_database),
                                self.utils.jsonschema(self.search_manager.search_chat_history)]

    def execute_function_call(self, function_name: str, function_args: dict):
        if function_name == "search_chat_history":
            return self.search_manager.search_chat_history(**function_args)
        elif function_name == "add_user_info_to_database":
            return self.chat_history_manager.add_user_info_to_database(**function_args)

    def chat(self, user_message):
        function_result = None
        search_term = None
        search_result_section = None
        chat_state = "thinking"
        function_call_count = 0  # Track function calls
        while chat_state != "finished":
            try:
                if isinstance(function_result, str):
                    search_result_section = f"""## Search Result:\n"
                    If you see this section, it means you have just requested a search based on the most recent user's question.
                    The search term you requested was: {search_term['search_term']}.
                    Here is the result of the search from the chat history database:\n{function_result}"""

                elif function_call_count >= self.cfg.max_function_calls and function_result == []:
                    search_result_section = f"""## Search Limit Reached.\n
                    You have requested a search multiple times for the term: {search_term['search_term']}
                    based on the most recent user's question, but no results were found.
                    Please conclude the conversation with the user based on the available information."""
                elif isinstance(function_result, bool):
                    search_result_section = f"""## User Info Updated\n
                    Your request to update the user's information was successful. Please continue the conversation with the user.
                    """
                system_prompt = prepare_system_prompt_for_agentic_chatbot_v1(self.user_manager.user_info,
                                                                             self.previous_summary,
                                                                             self.chat_history_manager.chat_history,
                                                                             search_result_section)
                print("--------------------------------")
                print(f"User info: {self.user_manager.user_info}")
                print(f"Previous summary: {self.previous_summary}")
                print(
                    f"Chat history: {self.chat_history_manager.chat_history}")
                print("--------------------------------")
                print(f"Search result section: {search_result_section}")
                print(f"System prompt: {system_prompt}")
                response = self.client.chat.completions.create(
                    model=self.chat_model,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_message}],
                    functions=self.agent_functions,
                    function_call="auto",
                    temperature=self.cfg.temperature
                )
                if response.choices[0].message.function_call:
                    function_call_count += 1  # Increment function call count
                    if function_call_count > self.cfg.max_function_calls:
                        chat_state = "finished"
                        continue  # Force response generation

                    function_name = response.choices[0].message.function_call.name
                    function_args = json.loads(
                        response.choices[0].message.function_call.arguments)
                    print(
                        f"Function call {function_call_count}: {function_name} with args {function_args}")
                    if function_name == "search_chat_history":
                        search_term = function_args
                        print(f"Search term: {search_term}")
                    print("function name:",
                          response.choices[0].message.function_call.name)
                    function_result = self.execute_function_call(response.choices[0].message.function_call.name,
                                                                 json.loads(
                                                                     (response.choices[0].message.function_call.arguments)))
                    print(f"Function result: {function_result}")
                elif response.choices[0].message.content:
                    assistant_response = response.choices[0].message.content
                    self.chat_history_manager.add_to_history(
                        user_message, assistant_response, self.max_history_pairs
                    )
                    self.chat_history_manager.update_chat_summary(
                        self.max_history_pairs, self.client, self.summary_model
                    )
                    chat_state = "finished"
                    return assistant_response

            except Exception as e:
                return f"Error: {str(e)}\n{format_exc()}"
