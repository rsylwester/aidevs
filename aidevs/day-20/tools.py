from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.documents import Document

import api_openai
import qdrant_facade

openai_client = ChatOpenAI(model="gpt-4")


def ask_gpt(question, system):
    answer = openai_client.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": question},
                ]),
            SystemMessage(
                content=[
                    {"type": "text", "text": f"Use information in context. ### Context: {system}"},
                ])]
    )

    return answer.content


class SaveMemoryTool(BaseModel):
    """
    If there is some kind information then it will be saved with this tool.
    """

    note: str = Field(..., description="note")

    @staticmethod
    def invoke(kwargs: dict):
        note = kwargs['note']
        print(f"saving memory {note}")

        qdrant_facade.save_documents(note)
        return "OK"

    @classmethod
    def name(cls):
        return cls.__name__


class AnswerTool(BaseModel):
    """
    If question is passed, then it is called to answer it.
    """

    question: str = Field(..., description="question")

    @staticmethod
    def invoke(kwargs: dict):
        question = kwargs['question']
        print(f"answers question: {question}")
        doc: Document = qdrant_facade.similarity_search(question)

        return ask_gpt(system=doc.page_content, question=question)

    @classmethod
    def name(cls):
        return cls.__name__
