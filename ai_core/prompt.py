from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = """


"""

BASE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])