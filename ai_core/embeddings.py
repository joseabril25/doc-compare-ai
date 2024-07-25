from typing import List, Type
from .parsing import File

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

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
    def set_retriever(cls, files: List[File]):
        documents = cls._combine_files(files)
        vector = FAISS.from_documents(documents, cls.embeddings)
        return vector.as_retriever()

def embed_files(files: List[File]):
    return FileIndex.set_retriever(files)