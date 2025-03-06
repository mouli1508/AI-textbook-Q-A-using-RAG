import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from utils.database_manager import DatabaseManager
from utils.user_manager import UserManager
from utils.chat_history_manager import ChatHistoryManager
from utils.search_manager import SearchManager
from utils.prepare_prompt import prepare_system_prompt_for_agentic_v1
from utils.utils import Utils
from pydantic import create_model
import inspect
from inspect import Parameter
from traceback import format_exc
import json

load_dotenv()


class Chatbot:
    def __init__(self,
                 chat_model: str = "gpt-4o-mini",
                 summary_model: str = "gpt-3.5-turbo",
                 max_history_pairs: int = 2,
                 temperature: float = 0):

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat_model = chat_model
        self.summary_model = summary_model
        self.temperature = temperature
        self.max_history_pairs = max_history_pairs

        self.session_id = str(uuid.uuid4())
        self.utils = Utils()
        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.chat_history_manager = ChatHistoryManager(
            self.db_manager, self.user_manager.user_id, self.session_id)
        self.previous_summary = self.chat_history_manager.get_latest_summary()

        self.search_manager = SearchManager(
            self.db_manager, self.utils, self.client, self.summary_model)
        self.agent_functions = [self.jsonschema(self.chat_history_manager.add_user_info_to_database),
                                self.jsonschema(self.search_manager.search_chat_history)]

    def jsonschema(self, f):
        """
        Generate a JSON schema for the input parameters of the given function.

        Parameters:
            f (FunctionType): The function for which to generate the JSON schema.

        Returns:
            Dict: A dictionary containing the function name, description, and parameters schema.
        """
        kw = {n: (o.annotation, ... if o.default == Parameter.empty else o.default)
              for n, o in inspect.signature(f).parameters.items()}
        s = create_model(f'Input for `{f.__name__}`', **kw).schema()
        return dict(name=f.__name__, description=f.__doc__, parameters=s)

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
        max_function_calls = 3
        while chat_state != "finished":
            try:
                if function_result:
                    search_result_section = f"""## If you see this section, it means you have just requested a search based on the most recent user's question.
                    The search term that you requested was {search_term["search_term"]}. Here is the result of the search for that word on chat history database:\n {function_result}"""

                system_prompt = prepare_system_prompt_for_agentic_v1(self.user_manager.user_info,
                                                                     self.previous_summary,
                                                                     self.chat_history_manager.chat_history,
                                                                     search_result_section)
                print(f"System prompt: {system_prompt}")
                response = self.client.chat.completions.create(
                    model=self.chat_model,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_message}],
                    functions=self.agent_functions,
                    function_call="auto",
                    temperature=0
                )
                if response.choices[0].message.function_call:
                    function_call_count += 1  # Increment function call count
                    if function_call_count > max_function_calls:
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

                elif function_call_count >= max_function_calls and response.choices[0].message.content == None:
                    search_result_section = f"""## If you see this section, it means you have requested the search based on the most recent user's question multiple times.
                    The results were provided to you after each search but you didn't conclude the conversation. Here is the result of the last search for that word on chat history database:\n{function_result}
                    \nConclude the conversation with the user based on what is provided to you."""
                    chat_state = "finished"
                    return assistant_response
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
