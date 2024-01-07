from .tool import ToolInterface


class GoToURL(ToolInterface):
    """Go to a specific url address"""

    name: str = "Go to a specific url web address"
    description: str = (
        'Change the url to a provied URL. Input format: {{"url":"<place_url_here>"}}'
    )
    click_on_screen: str = False
    example_script: str = "go_to_url"

    def process_tool_arg(self, **kwarg):
        url = kwarg["url"]
        return {"text": url}


class MessageUser(ToolInterface):
    """show text to the user"""

    name: str = "Textual Guidance"
    description: str = 'Present the user with a message, Input format: {{"text":"<text_to_enter>"}}'
    click_on_screen: str = False
    example_script: str = "show_guidance"

    def process_tool_arg(self, **kwarg):
        text = kwarg["text"]
        return {"text": text}
