from pyprojroot import here
import os
import chromadb
import uuid
from chromadb.utils import embedding_functions
from utils.config import Config


class VectorDBManager:
    def __init__(self,
                 config: Config
                 ):
        self.cfg = config()
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=self.cfg.embedding_model
        )
        self.db_client = chromadb.PersistentClient(
            path=str(self.cfg.vectordb_dir))
        self.db_collection = self.db_client.get_or_create_collection(
            name=self.cfg.collection_name,
            embedding_function=self.embedding_function,
        )

    def update_vector_db(self, msg_pair: dict):
        self.db_collection.add(
            ids=str(uuid.uuid4()),
            documents=[str(msg_pair)]
        )
        print(f"Vector DB updated.")
        return None
