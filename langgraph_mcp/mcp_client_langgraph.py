import asyncio
from typing import Annotated, Sequence, TypedDict

from langchain.chat_models import init_chat_model
from langchain.schema.messages import HumanMessage
from langchain_core.messages import BaseMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

model = init_chat_model("google_vertexai:gemini-2.0-flash", temperature=0)


class AgentState(TypedDict):
    """The state of the agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int


# Define the conditional edge that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    # If the last message is not a tool call, then we finish
    if not messages[-1].tool_calls:
        return "end"
    # default to continue
    return "continue"


# --- Main LangGraph Setup ---
async def main():

    client = MultiServerMCPClient(
        {
            "elementary_math": {
                "command": "python",
                "args": ["elementary_math_server.py"],
                "transport": "stdio",
            },
            "exponentiation_math": {
                "command": "python",
                "args": ["exponentiation_math_server.py"],
                "transport": "stdio",
            },
        }
    )
    # Load all MCP tools
    tools = await client.get_tools()

    # --- Gemini wrapper to simulate LangChain-style `invoke` + tool call handling ---
    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}

    # --- Build LangGraph ---
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.set_entry_point("call_model")
    builder.add_conditional_edges(
        "call_model",
        should_continue,
        {
            # If `tools`, then we call the tool node.
            "continue": "tools",
            # Otherwise we finish.
            "end": END,
        },
    )
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    # --- Input 1: Get best 3 deal IDs ---
    prompt1 = "what's (3 + 5) x 12?"
    print("🔍 Question 1:", prompt1)
    result1 = await graph.ainvoke({"messages": [HumanMessage(content=prompt1)]})

    for msg in result1["messages"]:
        print(f"{msg.type.upper()}: {msg.content}")

    # --- Input 2: Continue the same conversation with the previous context ---
    prompt2 = "Then I want to get its square number"
    print("🔍 Question 2:", prompt2)
    # print(result1["messages"])
    # Use the messages from result1 and add the new question
    continued_messages = result1["messages"] + [HumanMessage(content=prompt2)]
    result2 = await graph.ainvoke({"messages": continued_messages})

    # Print only the new messages (skip the ones we already printed)
    new_messages = result2["messages"][len(result1["messages"]) :]
    for msg in new_messages:
        print(f"{msg.type.upper()}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())
