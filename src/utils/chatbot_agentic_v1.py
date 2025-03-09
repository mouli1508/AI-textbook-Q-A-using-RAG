import os
import uuid
import json
from dotenv import load_dotenv
from openai import OpenAI
from traceback import format_exc
from utils.database_manager import DatabaseManager
from utils.user_manager import UserManager
from utils.chat_history_manager import ChatHistoryManager
from utils.search_manager import SearchManager
from utils.prepare_system_prompt import prepare_system_prompt_for_agentic_chatbot_v1
from utils.utils import Utils
from utils.config import Config

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
        self.agent_functions = [self.utils.jsonschema(self.user_manager.add_user_info_to_database),
                                self.utils.jsonschema(self.search_manager.search_chat_history)]

    def execute_function_call(self, function_name: str, function_args: dict):
        if function_name == "search_chat_history":
            return self.search_manager.search_chat_history(**function_args)
        elif function_name == "add_user_info_to_database":
            return self.user_manager.add_user_info_to_database(**function_args)

    def chat(self, user_message):
        function_call_result_section = ""
        function_call_state = None
        chat_state = "thinking"
        function_call_count = 0
        self.chat_history = self.chat_history_manager.chat_history
        function_call_prompt = f"""## You called the following functions:\n"""
        while chat_state != "finished":
            try:
                if function_call_state:
                    function_call_prompt += f"{function_call_count} {function_name}\n with the following arguments: {function_args}\n"
                    function_call_prompt += f"- State: {function_call_state}\n"
                    # I won't show the result of the function call in the chat history since it will be shown in the function call section.
                    self.chat_history.append(
                        (function_call_state, function_call_prompt))
                    function_call_result_section = function_call_prompt
                    function_call_result_section += f"- Result: {function_call_result}\n"

                elif function_call_count >= self.cfg.max_function_calls:
                    function_call_result_section = f"""  # Function Call Limit Reached.\n
                    Please conclude the conversation with the user based on the available information."""
                system_prompt = prepare_system_prompt_for_agentic_chatbot_v1(self.user_manager.user_info,
                                                                             self.previous_summary,
                                                                             self.chat_history,
                                                                             function_call_result_section)
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
                    function_call_count += 1
                    function_name = response.choices[0].message.function_call.name
                    function_args = json.loads(
                        response.choices[0].message.function_call.arguments)
                    self.chat_history.append(
                        f"Agent requested a function call: {function_name} with args {function_args}")
                    function_call_state, function_call_result = self.execute_function_call(
                        function_name, function_args)

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
