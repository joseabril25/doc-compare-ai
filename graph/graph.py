from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.messages import AIMessage, SystemMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.managed import IsLastStep

from graph.tools import web_search
from graph.prompts import initial_prompt

load_dotenv()
class State(MessagesState):
    is_last_step: IsLastStep

# set model - llama or gpt4o
# models = {
#     "gpt-4o-mini": ChatOpenAI(model="gpt-4o-mini", temperature=0.5, streaming=True),
#     "llama-3.1-70b": ChatGroq(model="llama-3.1-70b-versatile", temperature=0.5)
# }

model = ChatOpenAI(model="gpt-4o", temperature=0.5, streaming=True)
# model = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.5)


# set tools (web search *for now*)
tools = [web_search]

# Define the model callable
def wrap_model(model: BaseChatModel):
    model = model.bind_tools(tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=initial_prompt)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model

async def acall_model(state: State, config: RunnableConfig):
    # m = models[config["configurable"].get("model", "gpt-4o-mini")]
    model_runnable = wrap_model(model)
    response = await model_runnable.ainvoke(state, config)
    if state["is_last_step"] and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Build the graph
graph = StateGraph(State)
# add nodes
graph.add_node("model", acall_model)
graph.add_node("tools", ToolNode(tools))
# add entry point
graph.set_entry_point("model")

# add edges
graph.add_edge("tools", "model")

# After "model", if there are tool calls, run "tools". Otherwise END.
def pending_tool_calls(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    else:
        return END

# add conditional edges - if there are tool calls, run "tools". Otherwise END.
graph.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", END: END})
# graph.add_conditional_edges("model", tools_condition)

# compile the graph
career_assistant = graph.compile(checkpointer=MemorySaver())