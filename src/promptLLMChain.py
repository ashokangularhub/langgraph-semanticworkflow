from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import OpenAI, ChatOpenAI
from typing import TypedDict
from src.state import PromptLLMState

load_dotenv()

model = ChatOpenAI()


def generate_titleOutline(state: PromptLLMState) -> PromptLLMState:
    title = state['title']
    prompt = f'generate the outline for the following title :{title}'

    outline_value = model.invoke(prompt).content
    state['outline'] = outline_value
    return state


def generate_titleContent(state: PromptLLMState) -> PromptLLMState:
    outline_val = state['outline']
    prompt = f'generate good detailed content for this outline : {outline_val}'

    content_value = model.invoke(prompt).content
    state['content'] = content_value
    return state


graph = StateGraph(PromptLLMState)

graph.add_node('generate_titleOutline', generate_titleOutline)
graph.add_node('generate_titleContent', generate_titleContent)

graph.add_edge(START, 'generate_titleOutline')
graph.add_edge('generate_titleOutline', 'generate_titleContent')
graph.add_edge('generate_titleContent', END)

promptchain_workflow = graph.compile()
