from llama_index.core import VectorStoreIndex, Document
from llama_index.core.chat_engine.types import ChatMode, BaseChatEngine
from llama_index.core.indices.base import IndexType
from llama_index.llms.openai import OpenAI
from requests import Response

import api_aidevs
import env

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("whoami")

"""
Solution goes below
"""

llm = OpenAI(temperature=0.2, model="gpt-4", api_key=env.OPENAI_API_KEY)

rules_document = Document(text='''
Strict rules you’re obligated to follow throughout the conversation: 
- If you are sure of the answer then give short answer without comments
- If you don't know answer or you are unsure then say "-"
- always skip any additional comments. 
- Give answer if you are truly sure
''')

final_answer = None
vector_store_index: IndexType = VectorStoreIndex.from_documents(documents=[rules_document], llm=llm)

for i in range(10):
    task_json: dict = api_aidevs.get_task(token)
    hint = task_json['hint']

    vector_store_index.insert(Document(text=hint))

    engine: BaseChatEngine = vector_store_index.as_chat_engine(chat_mode=ChatMode.CONTEXT, llm=llm)
    answer = engine.chat("Who Is It?")

    print(f"Hint: {hint}")
    print(f"Answer: {answer}")

    if answer.response != '-':
        final_answer = answer.response
        break

"""
Sending solution of the task
"""
print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, final_answer, debug=True)
