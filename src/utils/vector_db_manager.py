from pyprojroot import here
import os
import chromadb
import uuid
from chromadb.utils import embedding_functions


class VectorDBManager:
    def __init__(self,
                 db_path: str,
                 embedding_model: str,
                 vectordb_dir: str,
                 collection_name: str,
                 ):
        self.db_path = db_path
        self.embedding_model = embedding_model
        self.vectordb_dir = here("data/vectordb")
        self.collection_name = "chat_history"
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=embedding_model
        )
        self.db_client = chromadb.PersistentClient(path=str(self.vectordb_dir))
        self.collection = self.db_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

    def update_vector_db(self, msg_pair: dict):
        return self.collection.add(
            ids=str(uuid.uuid4()),
            documents=[str(msg_pair)]
        )
