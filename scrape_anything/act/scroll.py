from .tool import ToolInterface


class ScrollDown(ToolInterface):
    """Scroll down the web page by half the screen height"""

    name: str = "Scroll Down"
    description: str = "Scroll down the web page by half the screen height, no input."
    example_script: str = "scroll_down"


class ScrollUp(ToolInterface):
    """Scroll up the web page by half the screen height"""

    name: str = "Scroll Up"
    description: str = "Scroll up the web page by half the screen height, no input."
    example_script: str = "scroll_up"


class ScrollRight(ToolInterface):
    """Scroll the web page to the right by half the screen width"""

    name: str = "Scroll Right"
    description: str = (
        "Scroll the web page to the right by half the screen width, no input"
    )
    example_script: str = "scroll_right"


class ScrollLeft(ToolInterface):
    """Scroll the web page to the left by half the screen width"""

    name: str = "Scroll Left"
    description: str = (
        "Scroll the web page to the left by half the screen width, no input"
    )
    example_script: str = "scroll_left"
