import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from pyprojroot import here
load_dotenv()


def prepare_vector_db():
    embedding_model = "text-embedding-3-small"
    vectordb_dir = here("data/vectordb")
    db_collection_name = "chat_history"
    openai_embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=embedding_model
    )
    if not os.path.exists(here(vectordb_dir)):
        # If it doesn't exist, create the directory and create the embeddings
        os.makedirs(here(vectordb_dir))
        print(f"Directory '{vectordb_dir}' was created.")
    db_client = chromadb.PersistentClient(path=str(vectordb_dir))
    db_collection = db_client.get_or_create_collection(
        name=db_collection_name,
        embedding_function=openai_embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
    print("DB collection created:", db_collection)
    print("DB collection count:", db_collection.count())


if __name__ == "__main__":
    prepare_vector_db()
