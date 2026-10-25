from typing import TypedDict

class TemperatureState(TypedDict):
    temp_foreignheit: float
    temp_celcius: float
    weather_label: str

class LLMQueryState(TypedDict):
    query: str
    response: str

class PromptLLMState(TypedDict):
    title: str
    outline:str
    content:str
