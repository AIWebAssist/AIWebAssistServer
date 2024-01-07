
from typing import List

class ToolDescriptionPromptValues:
    
    def __init__(self,tools:List) -> None:
        self.tools = tools

    def __str__(self) -> str:
        return "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

class ExecutionStatusPromptValues:

    def __init__(self) -> None:
        self.previous_responses = list()
        self.previous_tools = list()

    def is_empty(self):
        return len(self.previous_responses) == 0
    
    def set(self,tool,message):
        self.previous_responses.append(message)
        self.previous_tools.append(tool)

    def append(self,message):
        self.previous_responses[-1] += f"{self.previous_responses[-1]}. {message}."

    def __str__(self) -> str:
        return "\n".join(self.previous_responses)

class DataFramePromptValues:

    def __init__(self,on_screen) -> None:
        self.on_screen = on_screen

    def __str__(self) -> str:
        return self.on_screen.rename_axis("index").to_csv(float_format=f'%.2f')
        