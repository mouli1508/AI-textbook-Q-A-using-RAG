from pyprojroot import here
from yaml import load, Loader


class Config:
    def __init__(self):
        with open(here("config/config.yml"), "r") as f:
            config = load(f, Loader=Loader)
        self.db_path = here(config["directories"]["db_path"])
        self.vectordb_dir = here(config["directories"]["vectordb_dir"])
        self.chat_model = config["llm_config"]["chat_model"]
        self.summary_model = config["llm_config"]["summary_model"]
        self.temperature = config["llm_config"]["temperature"]
        self.max_history_pairs = config["chat_history_config"]["max_history_pairs"]
        self.max_characters = config["chat_history_config"]["max_characters"]
        self.num_retrieved_content = config["search_config"]["num_retrieved_content"]
        self.max_function_calls = config["agent_config"]["max_function_calls"]
        self.collection_name = config["vectordb_config"]["collection_name"]
        self.embedding_model = config["vectordb_config"]["embedding_model"]
