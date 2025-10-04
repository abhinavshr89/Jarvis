from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_ollama import ChatOllama
from langchain.agents import Tool
from langchain_core.tools import tool
import os
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
import sqlite3
from langchain_core.messages import SystemMessage

from commands import open_youtube, search_google, open_notepad, end_program, take_screenshot, get_time, mute_volume

# Chat model (Ollama LLM)
llm = ChatOllama(model="llama3.2")



# Define tools - use the decorated functions directly
tools = [open_youtube, search_google, open_notepad, take_screenshot, get_time, mute_volume, end_program]

# ✅ Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


# ✅ Define proper state schema
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ✅ Create chat function with system message
def chatbot(state: State):
    # Add system message if not present
    messages = state["messages"]
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        system_msg = system_msg = SystemMessage(content="""You are a helpful voice assistant. 

        Rules:
        1. Default mode is plain conversation. 
        - Greet, answer, and chat normally.
        2. Tools are ONLY for explicit requests:
        - "Open YouTube" or "Search YouTube for [query]" → use open_youtube with query parameter
        - "Search Google" → use open_google
        - "Open Notepad" → use open_notepad
        - "Take Screenshot" → use take_screenshot
        - "Get Time" → use get_time
        - "Mute Volume" → use mute_volume
        - "End program" → use end_program
        3. When user says "open YouTube and search for X", extract X as the query parameter.
        4. Never call tools for greetings, small talk, or general questions.
        """)

        messages = [system_msg] + messages
    
    return {"messages": [llm_with_tools.invoke(messages)]}

# Define state graph
graph = StateGraph(State)

# Add LLM node (chat handling)
graph.add_node("chat", chatbot)

# Add tool execution node
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

# Flow setup
graph.add_edge(START, "chat")
graph.add_conditional_edges("chat", tools_condition)
graph.add_edge("tools", "chat")
graph.add_edge("chat", END)

# ✅ Ensure directory exists
os.makedirs("./voice_assistant/memory", exist_ok=True)

# ✅ Create checkpointer with direct connection
db_path = str(Path(__file__).parent / "checkpoints.sqlite3")
conn = sqlite3.connect(db_path, check_same_thread=False)
checkpointer = SqliteSaver(conn)

app = graph.compile(checkpointer=checkpointer)

# ✅ Create run_agent function for main.py
def run_agent(user_input: str, thread_id: str = "user1") -> str:
    """Run the agent with user input and return the response."""
    config = {"configurable": {"thread_id": thread_id}}
    response = app.invoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    
    # Extract the last message content
    if response and "messages" in response:
        last_message = response["messages"][-1]
        return last_message.content if hasattr(last_message, 'content') else str(last_message)
    return "No response"



