import uvicorn
from fastapi import FastAPI
from src.temperatureConversion import workflow
from pydantic import BaseModel
from fastapi.responses import Response
from src.llmQuery import llm_workflow
from src.promptLLMChain import promptchain_workflow

apiapp = FastAPI(title="Temperature conversion workflow with langgraph")


class TempRequest(BaseModel):
    temp_foreignheit: float


class TempResponse(BaseModel):
    temp_celcius: float
    temp_foreignheit: float
    weather_label: str


class LLMRequest(BaseModel):
    user_query: str


class LLMResponse(BaseModel):
    user_query: str
    response: str

class PromptChainLLmRequest(BaseModel):
    title:str

class PromptChainLLmResponse(BaseModel):
    title:str
    outline:str
    content:str


@apiapp.post("/convert_temperature", response_model=TempResponse)
def run_workflow(request: TempRequest):
    initial_state = {"temp_foreignheit": request.temp_foreignheit}
    final_state = workflow.invoke(initial_state)
    return TempResponse(
        temp_celcius=final_state["temp_celcius"],
        temp_foreignheit=final_state["temp_foreignheit"],
        weather_label=final_state["weather_label"],
    )


@apiapp.get("/graph/image")
def get_graph_image():
    png_bytes = workflow.get_graph().draw_mermaid_png()
    return Response(content=png_bytes, media_type="image/png")


@apiapp.post("/query_llm", response_model=LLMResponse)
def query_llm(request: LLMRequest):
    initial_state = {"query": request.user_query}
    final_state = llm_workflow.invoke(initial_state)
    return LLMResponse(
        response=final_state["response"],
        user_query=final_state["query"]
    )


@apiapp.get("/graph/sequencellmFlow")
def get_sequence_llmflow_image():
    png_bytes = llm_workflow.get_graph().draw_mermaid_png()
    return Response(content=png_bytes, media_type="image/png")


@apiapp.post("/promptchain_llmquery", response_model=PromptChainLLmResponse)
def generate_titleContent(request : PromptChainLLmRequest):
    initial_state = {"title" : request.title}
    
    final_state = promptchain_workflow.invoke(initial_state)
    promptChainLLmResponse = PromptChainLLmResponse(
       title=  final_state['title'],
        outline = final_state['outline'],
        content = final_state['content']
    )
    return promptChainLLmResponse

@apiapp.get("/graph/promptChainllmFlow")
def get_sequence_promptchain_llm_image():
    png_bytes = promptchain_workflow.get_graph().draw_mermaid_png()
    return Response(content=png_bytes, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(apiapp, host="0.0.0.0", port=8000)
