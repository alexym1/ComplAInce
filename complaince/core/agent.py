"""Core of the AI agent."""


from dotenv import load_dotenv
from langchain.schema import BaseMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
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
    builder.add_conditional_edges(
        "Assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )

    react_graph = builder.compile()

    return react_graph


@tracing_messages
def run_agent(prompt: str) -> list[HumanMessage]:
    """
    Run AI agent.

    Parameters
    ----------
    prompt
        natural language

    Returns
    -------
    Lists of messages embedded in a dictionnary
    """
    react_graph = create_agent()
    messages = [HumanMessage(content=prompt)]
    messages = react_graph.invoke({"messages": messages})

    return messages
