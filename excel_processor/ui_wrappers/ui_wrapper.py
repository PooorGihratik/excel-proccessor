from typing import Generic, TypeVar
from .console_ui import ConsoleUI


class UIWrapper:
    ui_item: ConsoleUI

    def __init__(self, ui: ConsoleUI):
        self.ui_item = ui


T = TypeVar("T", bound=UIWrapper)


class UIWrapable(Generic[T]):
    _ui_wrapper: T

    def set_ui(self, ui: ConsoleUI):
        if ui is not None:
            self._ui_wrapper = T.__init__(ui)
