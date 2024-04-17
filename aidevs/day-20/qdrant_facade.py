from typing import List

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

qdrant_client = QdrantClient(host="localhost", port=6333)
embeddings = OpenAIEmbeddings()

store: Qdrant = Qdrant(
    embeddings=embeddings,
    client=qdrant_client,
    collection_name="langchain-collection",
)


def save_documents(text: str):
    store.add_documents(documents=[Document(page_content=text)])


def similarity_search(text: str):
    doc: List[Document] = store.similarity_search(query=text)
    print("")
