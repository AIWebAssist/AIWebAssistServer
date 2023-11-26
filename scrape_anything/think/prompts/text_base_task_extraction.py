from pydantic import BaseModel

class TaskExtractionTextBasePrompt(BaseModel):

    final_answer_token:str = "Final Answer"
    observation_token:str = "Observation"
    

    prompt_template:str = f"""
    Today is {{today}}, the site you're looking on is {{site_url}}.

    Here is a representation of the valuable elements existing on the screen:
    {{on_screen_data}}

    Current screen dimensions: 
    {{screen_size}}

    Scroll Options: 
    {{scroll_ratio}}

    You should guide the user to complete the task given to you using the following tools:
    {{tool_description}}

    --
    Task To Accomplish: {{task_to_accomplish}}
    Previous executions:
    {{previous_responses}}
    ---
    Describe all Input Field:
      1. Element Index
      2. Coordinates
      3. Current Value
      4. Purpose

    Describe all Buttons:
      1. Element Index
      2. Coordinates
      3. Purpose

    Then describe:

    Question: The input question you must answer.
    Thought: Comment on what you want to do next.
    Execution Status: Comment on if the your previous executions what is successful.
    Current Task: comment on given the task and the past execution, what it your current goal.
    Action: The action to take, exactly one element of [{{tool_names}}]
    Action Input: The input to the action
    {observation_token}: The change you expect to see after the action is executed.
    {final_answer_token}: Your final message to the user if you think there task was accomplished.
    """

    def get_stop_patterns(self):
        return [f'\n{self.observation_token}', f'\n\t{self.observation_token}']

    def get_final_answer_token(self):
        return self.final_answer_token

    def format_prompt(self,**kwrgs):
        return  self.prompt_template.format(**kwrgs)