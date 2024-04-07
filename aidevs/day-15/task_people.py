import re

import requests
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import qdrant_client
from requests import Response

import api_aidevs
import api_openai
import env

Settings.embed_model = HuggingFaceEmbedding(model_name="allegro/herbert-large-cased")

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("people")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""


class VectorDbManager:
    COLLECTION_NAME = "people"

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

    def save_documents(self, documents: dict):
        for key, value in documents.items():
            document = Document(
                text=key,
                metadata={'name': key}
            )
            self.vector_store_index.insert(document)


def extract_name(question):
    pattern = r"\b[A-Z][a-z]*\s[A-Z][a-z]*\b"

    # Search for the pattern in the sentence
    match = re.search(pattern, question)

    if match:
        # Extract the matched name
        name = match.group()
        print(name)

        return name
    else:
        print("No name found")


def remove_redundant_keys(person: dict):
    return {
        'imie': person['imie'],
        'nazwisko': person['nazwisko'],
        'o_mnie': person['o_mnie'],
        'ulubiony_kolor': person['ulubiony_kolor']
    }


url_json_file = task_json['data']
question = task_json['question']
q_name = extract_name(question)

print(f"q_name {q_name}")

response = requests.get(url_json_file)
people_json = response.json()

people_dict: dict = dict()

for person in people_json:
    first_name = person['imie']
    last_name = person['nazwisko']
    people_dict[f"{first_name} {last_name}"] = remove_redundant_keys(person)

vector_db: VectorDbManager = VectorDbManager()

if not vector_db.vector_db_has_collection():
    vector_db.save_documents(people_dict)

result = vector_db.search_in_qdrant_collection(Settings.embed_model.get_text_embedding(q_name))
name = result[0].payload['name']

system = f"""
Always skip any additional comments. 
Use context for answering question.
Answer shortly eg.

Ulubiony kolor Agnieszki Rozkaz, to? -> bordowy

### Context ###
{people_dict[name]} 
"""
answer = api_openai.ask_gpt(system=system, question=question)

print(people_dict[name])

"""
Sending solution of the task
"""
print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, answer, debug=True)
