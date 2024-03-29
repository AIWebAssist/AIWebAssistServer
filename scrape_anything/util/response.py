import re
import json
from typing import Tuple


def extract_tool_and_args(generated: str) -> Tuple[str, str]:
    if "Action" in generated or "Action Input" in generated:
        if "Action Input" in generated:  # try to get actions with inputs
            regex = r"Action: [\[]?(.*?)[\]]?[\n]*Action Input:"
            match = re.search(regex, generated + "\n", re.DOTALL)
            if not match:
                raise ValueError(
                    f"the output `{generated}` is not matching the expected format."
                )
            tool = match.group(1).strip()

            regex = r"(?<=Action Input:)([\w\W]+?)(?=\})"
            match = re.search(regex, generated + "\n", re.DOTALL)
            if match:
                tool_input = match.group(1).strip()
            else:
                tool_input = "{"

            tool_input += "}"

        elif "Action" in generated:  # if not, try to get actions that have no input
            tool = generated.split("Action:")[-1].split("\n")[0].strip()
            tool_input = "{}"

        if "Current Action Goal" in generated:
            current_task = (
                generated.split("Current Action Goal:")[-1].split("\n")[0].strip()
            )
        else:
            current_task = "not provided."

        if "Next Action Goal" in generated:
            next_task = generated.split("Next Action Goal:")[-1].split("\n")[0].strip()
        else:
            next_task = "not provided."

    else:
        raise ValueError(
            f"you should provide one of the following: "
            f"('Action Input' and 'Action') or (only 'Action')"
        )

    try:
        tool_input = strip_characther_in_args(tool_input)
        tool_input = json.loads(tool_input)
    except json.JSONDecodeError:
        tool_input = {}
    return strip_tool(tool), tool_input, current_task, next_task


def strip_tool(string: str):
    return re.sub(r"[^a-zA-Z ]", "", string).strip(" ").strip('"')


def strip_characther_in_args(string: str):
    string_temp = string.strip(" ").strip('"').strip("None").strip("\n")
    string_temp = "{" + string_temp.split("{")[-1]
    string_temp = string_temp.split("}")[0] + "}"
    return string_temp


def parse_json(tool_input: str):
    try:
        response = json.loads(tool_input)
    except Exception as e:
        raise ValueError(f"the output `{tool_input}` is not a JSON, error = {e}") from e
    return response
