from typing import Generic, TypeVar
from .console_ui import ConsoleUI, LoadingContext
from .mock_ui import MockUI


class UIWrapper:
    ui_item: MockUI | ConsoleUI

    def __init__(self, ui: MockUI | ConsoleUI):
        self.ui_item = ui


T = TypeVar("T", bound=UIWrapper)


class UIWrapable:
    _ui_wrapper = MockUI
    _base_class: Generic[T]

    def __init__(self, base_class: Generic[T]):
        self._ui_wrapper = base_class(ui=MockUI())
        self._base_class = base_class

    def set_ui(self, ui: ConsoleUI | MockUI):
        if ui is not None:
            self._ui_wrapper = self._base_class(ui)
