import threading
from enum import Enum


class IncommingData:
    viewpointscroll: int
    viewportHeight: int
    scroll_width: int
    scroll_height: int

    # f"width={width},height={height}"
    width: str
    height: str

    # data from the screen
    raw_on_screen: list
    screenshot: str

    def __init__(
        self,
        url,
        task,
        viewpointscroll,
        viewportHeight,
        scroll_width,
        scroll_height,
        width,
        height,
        raw_on_screen,
        screenshot,
    ) -> None:
        self.viewpointscroll = viewpointscroll
        self.viewportHeight = viewportHeight
        self.scroll_width = scroll_width
        self.scroll_height = scroll_height
        self.width = width
        self.height = height
        self.raw_on_screen = raw_on_screen
        self.url = url
        self.task = task
        self.screenshot = screenshot


class EnabledActions(Enum):
    ClickOnCoordinates = 0
    EnterText = 1
    GoBack = 2
    ScrollRight = 3
    ScrollUp = 4
    ScrollDown = 5
    Refresh = 6
    HitAKey = 7
    MessageUser = 8
    FinalMessage = 9
    ScrollLeft = 10
    GoToURL = 11

    def get_tool_enum(tool):
        return type(tool).__name__

    def filter_enabled(possible_tools):
        return list(
            filter(
                lambda x: EnabledActions.get_tool_enum(x)
                in EnabledActions.__members__.keys(),
                possible_tools,
            )
        )


class OutGoingData:
    def __init__(
        self, script: str, tool_input, session_closed: bool, force_guide: bool
    ) -> None:
        self.script = script
        self.tool_input = tool_input
        self.session_closed = session_closed
        self.force_guide = force_guide


class IncomeingExecutionReport:
    def __init__(self, data, close=False) -> None:
        self.data = data
        self.close = close

    def set_close(self):
        self.close = True

    def is_closed(self):
        return self.close


class IncomeingExecutionFailure:
    def __init__(self, message) -> None:
        self.message = message


class ClientResponseStatus(Enum):
    Failed = 0
    Successful = 1
    Close = 2


class LLMResponseParsingStatus(Enum):
    Failed = 0
    Successful = 1


class AgnetStatus(object):
    is_open = True

    def close(self):
        self.is_open = False

    def is_closed(self):
        return not self.is_open


class Error:
    def __init__(
        self,
        error_message,
        is_fatel=False,
        user_should_retry=False,
        session_closed=False,
    ) -> None:
        self.error_message = error_message
        self.is_fatel = is_fatel
        self.user_should_retry = user_should_retry
        self.session_closed = session_closed
