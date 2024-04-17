from pydantic import BaseModel, Field

import api_openai
import qdrant_facade


class SaveMemoryTool(BaseModel):
    """
    Saving passed memory
    """

    note: str = Field(..., description="note")

    @staticmethod
    def invoke(kwargs: dict):
        note = kwargs['note']
        print(f"saving memory {note}")

        qdrant_facade.save_documents(note)

    @classmethod
    def name(cls):
        return cls.__name__


class AnswerTool(BaseModel):
    """
    Answers on given questions
    """

    question: str = Field(..., description="question")

    @staticmethod
    def invoke(kwargs: dict):
        question = kwargs['question']
        print(f"answers question: {question}")
        doc: str = qdrant_facade.similarity_search(question)

        api_openai.ask_gpt(system=doc, question=question)

    @classmethod
    def name(cls):
        return cls.__name__
