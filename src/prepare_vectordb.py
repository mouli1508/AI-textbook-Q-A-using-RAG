import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from pyprojroot import here
from utils.config import Config

load_dotenv()


def prepare_vector_db():
    CFG = Config()
    openai_embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=CFG.embedding_model
    )
    if not os.path.exists(here(CFG.vectordb_dir)):
        # If it doesn't exist, create the directory and create the embeddings
        os.makedirs(here(CFG.vectordb_dir))
        print(f"Directory '{CFG.vectordb_dir}' was created.")
    db_client = chromadb.PersistentClient(path=str(CFG.vectordb_dir))
    db_collection = db_client.get_or_create_collection(
        name=CFG.collection_name,
        embedding_function=openai_embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
    print("DB collection created:", db_collection)
    print("DB collection count:", db_collection.count())


if __name__ == "__main__":
    prepare_vector_db()
