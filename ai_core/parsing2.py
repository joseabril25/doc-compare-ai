from io import BytesIO
import re
from hashlib import md5

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class File():
    def __init__(self, path):
        self.path = path
        self.loader = None
        self.vector = FAISS()
        self.embeddings = OpenAIEmbeddings()
    
    def create_vector_retriever(self, text):
        vector = FAISS.from_documents(text, self.embeddings)
        return vector.as_retriever()
    
    def strip_consecutive_newlines(text: str) -> str:
        """Strips consecutive newlines from a string
        possibly with whitespace in between
        """
        return re.sub(r"\s*\n\s*", "\n", text)
    
    def chunk_file(
        file: File, chunk_size: int, chunk_overlap: int = 0, model_name="gpt-3.5-turbo"
    ) -> File:
        """Chunks each document in a file into smaller documents
        according to the specified chunk size and overlap
        where the size is determined by the number of tokens for the specified model.
        """

        # split each document into chunks
        chunked_docs = []
        for doc in file.docs:
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                model_name=model_name,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            chunks = text_splitter.split_text(doc.page_content)

            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "page": doc.metadata.get("page", 1),
                        "chunk": i + 1,
                        "source": f"{doc.metadata.get('page', 1)}-{i + 1}",
                    },
                )
                chunked_docs.append(doc)

        chunked_file = file.copy()
        chunked_file.docs = chunked_docs
        return chunked_file
    
    @classmethod
    def read_file_and_chunk(cls, file: BytesIO):
        pdf = fitz.open(stream=file.read(), filetype="pdf")  # type: ignore
        docs = []
        for i, page in enumerate(pdf):
            text = page.get_text(sort=True)
            text = cls.strip_consecutive_newlines(text)
            doc = Document(page_content=text.strip())
            doc.metadata["page"] = i + 1
            doc.metadata["source"] = f"p-{i+1}"
            docs.append(doc)
        # file.read() mutates the file object, which can affect caching
        # so we need to reset the file pointer to the beginning
        file.seek(0)
        read_file = cls(name=file.name, id=md5(file.read()).hexdigest(), docs=docs)


    