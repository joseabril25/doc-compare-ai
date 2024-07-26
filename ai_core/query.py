

from typing import List
from pydantic import BaseModel

from langchain.docstore.document import Document
from langchain_core.runnables.base import Runnable
from langchain_core.messages import HumanMessage, AIMessage


class AnswerWithSources(BaseModel):
    answer: str
    question: str

def query(query: str, chain: Runnable) -> AnswerWithSources:
    chat_history = []
    result = chain.invoke({
        "chat_history": chat_history,
        "input": query
    })

    answer = result["answer"]

    return AnswerWithSources(answer=answer, question=query)