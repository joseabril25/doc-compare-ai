
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chat_models.base import BaseChatModel

def get_base_llm(open_ai_key) -> BaseChatModel:
    return OpenAI(temperature=0.7, openai_api_key=open_ai_key)

def get_agent_llm(open_ai_key) -> BaseChatModel:
    return ChatOpenAI(temperature=0.7, openai_api_key=open_ai_key)

