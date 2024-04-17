from typing import List

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

qdrant_client = QdrantClient(host="localhost", port=6333)
embeddings = OpenAIEmbeddings()

COLLECTION_NAME = "ownapipro"

store: Qdrant = Qdrant(
    embeddings=embeddings,
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
)

# if not qdrant_client.collection_exists(COLLECTION_NAME):
qdrant_client.recreate_collection(collection_name=COLLECTION_NAME, vectors_config={"size": 1536, "distance": "Cosine"})


def save_documents(text: str):
    store.add_documents(documents=[Document(page_content=text, metadata={"text": text})])


def similarity_search(text: str):
    docs: List[Document] = store.similarity_search(query=text)
    return docs[0] if docs else ""
