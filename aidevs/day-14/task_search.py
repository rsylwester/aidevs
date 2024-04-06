import json
import os
import shelve
from typing import List
from urllib.parse import urlparse

import qdrant_client
import requests
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client.grpc import ScoredPoint
from requests import Response

import api_aidevs
import env

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("search")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""
QUESTION = task_json['question']
ARCHIVE_URL = "https://unknow.news/archiwum_aidevs.json"

Settings.embed_model = OpenAIEmbedding()
query_vector = Settings.embed_model.get_text_embedding(QUESTION)


def extract_filename(url):
    # Parse the URL to get the path
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Extract the last part of the path
    last_part = os.path.basename(path)
    return last_part


def download_file(url, filename):
    response = requests.get(url)

    # Ensure the request was successful
    response.raise_for_status()

    with open('archiwum_aidevs.json', 'w') as file:
        file.write(response.text)

    return filename


def load_json_documents(filename):
    with open(filename, 'r') as file:
        return json.load(file)


class ShelveDBManager:
    MYDB_NAME = "shelve_db"

    @classmethod
    def save_documents_key_value_db(cls, documents):
        # Create or open a shelve database file
        with shelve.open(cls.MYDB_NAME) as db:
            for index, document in enumerate(documents):
                document['id'] = str(index)
                db[document['id']] = document

            db.close()

    @classmethod
    def read_docs_from_db(cls):
        documents = []
        with shelve.open(cls.MYDB_NAME) as db:
            for key in db.keys():
                documents.append(db[key])
            db.close()
        return documents

    @classmethod
    def get_doc(cls, id):
        with shelve.open(cls.MYDB_NAME) as db:

            if id in db:
                doc_id = db[id]
                return doc_id
            else:
                print(f'document with id [{id}] not found in shelve db')

            db.close()
        return None

    @classmethod
    def save_documents_from_remote_json_file(cls, url):
        filename = download_file(ARCHIVE_URL, extract_filename(url))
        documents = load_json_documents(filename)
        ShelveDBManager.save_documents_key_value_db(documents=documents)


class VectorDbManager:
    COLLECTION_NAME = "mycollection"

    def __init__(self):
        self.client = self.qdrant_client()

    def vector_db_has_collection(self):
        collections_info = self.client.get_collections().collections
        existing_collections = [col.name for col in collections_info]
        return VectorDbManager.COLLECTION_NAME in existing_collections

    def search_in_qdrant_collection(self, query):
        response = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=query,
            query_filter=None,  # Use this if you want to apply filters based on metadata
            limit=5,  # Adjust based on how many similar documents you want to retrieve
        )

        return response

    def qdrant_client(self):
        return qdrant_client.QdrantClient(
            env.QDRANT_URL,
            api_key=None,  # Use None for a local instance
        )

    @property
    def vector_store_index(self):
        vector_store: QdrantVectorStore = QdrantVectorStore(
            collection_name=VectorDbManager.COLLECTION_NAME,
            client=self.client,
        )

        return VectorStoreIndex.from_vector_store(vector_store=vector_store)

    def delete_collection(self):
        self.client.delete_collection(collection_name=VectorDbManager.COLLECTION_NAME)

    def save_documents(self, documents):
        for document in documents:
            document = Document(
                text=document.get("title", ""),  # Use the document title or main text
                id_=document["id"],
                metadata={
                    "url": document["url"],
                },  # Use the entire document as metadata
            )
            self.vector_store_index.insert(document)


vector_db_manager: VectorDbManager = VectorDbManager()

# read documents from key,value db if there are already
documents = ShelveDBManager.read_docs_from_db()

# if document not downloaded yet then download them and save into key,value DB
if not documents:
    ShelveDBManager.save_documents_from_remote_json_file(ARCHIVE_URL)
    documents = ShelveDBManager.read_docs_from_db()

# if documents not yet in vector database
if not vector_db_manager.vector_db_has_collection():
    vector_db_manager.save_documents(documents)

search_result: List[ScoredPoint] = vector_db_manager.search_in_qdrant_collection(query_vector)
best_hit = search_result[0]
best_hit_payload = search_result[0].payload

doc_id = best_hit_payload['doc_id']
url = best_hit_payload['url']

# whole document retrieving from shelve db - just optional step in context of this task
whole_doc = ShelveDBManager.get_doc(doc_id)

if whole_doc:
    print(f"Document ID: {doc_id}, Score: {best_hit.score}, URL: {url}")
print(f"Whole document retrieved from key,value DB: {whole_doc}")

"""
Sending solution of the task
"""
print("***** Sending answer *****")
search_result: Response = api_aidevs.send_answer(token, url, debug=True)
