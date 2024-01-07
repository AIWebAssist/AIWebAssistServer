import json
from ..util import Logger
from .base_llm import LLMInterface

class TestAllTools(LLMInterface):
    NO_INPUT_INSTRACTION:str = "no input"
    INSTRACTION_TO_REPLACED_WITH_NUMBER:str = "<place_num_here>"
    INSTRACTION_TO_REPLACED_WITH_STRING:str = "<text_to_enter>"
    INSTRACTION_TO_REPLACED_WITH_URL:str = "<place_url_here>"

    def description_to_json(self,tool_description):
        if self.NO_INPUT_INSTRACTION not in tool_description:
            excepted_format = "{" + tool_description.split("{")[-1].split("}")[0] + "}"
            excepted_format_after_populated = excepted_format.replace(
                self.INSTRACTION_TO_REPLACED_WITH_NUMBER, "1"
            ).replace(self.INSTRACTION_TO_REPLACED_WITH_STRING, "This will be LLM genrated text"
            ).replace(self.INSTRACTION_TO_REPLACED_WITH_URL, "www.example.com")

            return json.loads(excepted_format_after_populated)
        else:
            return json.loads('{}')
        
    def make_a_decide_on_next_action(
        self, num_loops: int, _: str, **prompt_params
    ):
        
        tool_descriptions = prompt_params['tool_description']
        tool_executing = list(filter(lambda x:x.example_script  == prompt_params['task_to_accomplish'] , tool_descriptions.tools))
        if len(tool_executing) == 1:
            Logger.debug(f"executing by example script {prompt_params['task_to_accomplish']}")
            selected_tool = tool_executing[0]
        else:
            selected_tool = tool_descriptions.tools[num_loops%len(tool_descriptions.tools)]

        args = self.description_to_json(selected_tool.description)
        if selected_tool.click_on_screen: # [ prompt_params['on_screen_data'].on_screen.clickable]
            
            location_prex = prompt_params['on_screen_data'].on_screen[['centerX','centerY']].sum(axis=1).sort_values()
            something_to_click_on  = prompt_params['on_screen_data'].on_screen.sample(1,weights=location_prex.values)
            args['x'] = something_to_click_on.iloc[0]['centerX']
            args['y'] = something_to_click_on.iloc[0]['centerY']
        
        return f"""
        Action: {selected_tool.name}
        Action Input: {json.dumps(args)}
        """