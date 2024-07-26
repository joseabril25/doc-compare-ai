import streamlit as st
from typing import List, Type

from ai_core.prompt import BASE_PROMPT, DOC_PROMPT
from .parsing import File

from langchain.vectorstores.faiss import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chat_models.base import BaseChatModel
from langchain.chains.combine_documents import create_stuff_documents_chain

class FileIndex:
    def __init__(self, files: List[Type[File]]):
        self.files = files
        self.embeddings = OpenAIEmbeddings()

    @staticmethod
    def _combine_files(files: List[File]) -> List[Document]:
        """Combines all the documents in a list of files into a single list."""

        all_texts = []
        for file in files:
            for doc in file.docs:
                doc.metadata["file_name"] = file.name
                doc.metadata["file_id"] = file.id
                all_texts.append(doc)

        return all_texts
    
    @classmethod
    def set_retriever(cls, files: List[File], key: str):
        documents = cls._combine_files(files)
        embeddings = OpenAIEmbeddings(openai_api_key=key)
        vector = FAISS.from_documents(documents, embeddings)
        return vector.as_retriever()

def create_chain(files: List[File]):
    openai_api_key = st.session_state.get("OPENAI_API_KEY")
    llm = OpenAI(openai_api_key=openai_api_key)
    retriever = FileIndex.set_retriever(files, openai_api_key)
    retriever_chain = create_history_aware_retriever(llm, retriever, BASE_PROMPT)
    document_chain = create_stuff_documents_chain(llm, DOC_PROMPT)
    return create_retrieval_chain(retriever_chain, document_chain)