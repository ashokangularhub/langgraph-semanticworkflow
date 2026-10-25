from langgraph.graph import StateGraph,START,END
from src.state import TemperatureState

def convert_temperatur(state : TemperatureState) -> TemperatureState:
    foreignHeit_temp =  state['temp_foreignheit'] 
    celcius_temp = (foreignHeit_temp - 32) * 5.0/9.0
    state['temp_celcius'] = round(celcius_temp,2)
    return state

def label_weather(state: TemperatureState) -> TemperatureState:
    celcius_temp = state['temp_celcius']
    if(celcius_temp<30):
        state['weather_label'] = 'cold'
    elif(celcius_temp > 30 and celcius_temp < 50):
        state['weather_label'] = 'warm'
    elif(celcius_temp >=50):
        state['weather_label']= 'hot'
    return state

graph = StateGraph(TemperatureState)

## add nodes that perform some action
graph.add_node('convert_temperatur',convert_temperatur)
graph.add_node('label_weather',label_weather)

## add edges that define the flow
graph.add_edge(START,'convert_temperatur')
graph.add_edge('convert_temperatur','label_weather')
graph.add_edge('label_weather',END)



## compile graph

workflow = graph.compile()