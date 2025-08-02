"""Core of the AI agent."""

import uuid

from dotenv import load_dotenv
from langchain.schema import BaseMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from complaince.core.agent_tools import (
    clone_github_repository,
    map_api_structure_tool,
    map_git_history_tool,
    map_repo_structure_tool,
)
from complaince.core.monitoring import tracing_messages

load_dotenv()


tools = [clone_github_repository, map_repo_structure_tool, map_api_structure_tool, map_git_history_tool]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


def create_assistant(state: MessagesState) -> dict[str, list[BaseMessage]]:
    """
    Assistant to generate AI agents.

    Parameters
    ----------
    state
        State of the messages

    Returns
    -------
    Lists of messages embedded in a dictionnary
    """
    sys_msg = SystemMessage(
        content="""You are a helpful assistant tasked with mapping a GitHub repository using available tools.
        Use previous tool outputs to guide next steps."""
    )
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


def create_agent():
    """Create AI agent."""
    builder = StateGraph(MessagesState)

    # Define nodes
    builder.add_node("Assistant", create_assistant)
    builder.add_node("tools", ToolNode(tools))

    # Define edges
    builder.add_edge(START, "Assistant")
    builder.add_conditional_edges("Assistant", tools_condition)
    builder.add_edge("tools", "Assistant")

    react_graph = builder.compile(checkpointer=MemorySaver())

    return react_graph


@tracing_messages
def run_agent(prompt: str, thread_id: str | None = None) -> list[HumanMessage]:
    """
    Run AI agent.

    Parameters
    ----------
    prompt
        natural language

    thread_id
        ID of the discussion thread

    Returns
    -------
    Lists of messages embedded in a dictionnary
    """
    react_graph = create_agent()

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    messages = [HumanMessage(content=prompt)]
    messages = react_graph.invoke({"messages": messages}, config={"configurable": {"thread_id": thread_id}})

    return messages
