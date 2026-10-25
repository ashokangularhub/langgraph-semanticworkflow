from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from typing import TypedDict
from src.state import LLMQueryState

load_dotenv()
model = ChatOpenAI()


def query_llm(state: LLMQueryState) -> LLMQueryState:
    user_query = state["query"]
    prompt = f"answer the user query :{user_query}"

    response = model.invoke(prompt).content
    state["response"] = response
    return state


graph1 = StateGraph(LLMQueryState)

graph1.add_node("query_llm", query_llm)

graph1.add_edge(START, "query_llm")
graph1.add_edge("query_llm", END)

llm_workflow = graph1.compile()
