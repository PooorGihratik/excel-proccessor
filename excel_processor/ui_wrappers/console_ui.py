from rich.console import Console
from rich.progress import (
    Task,
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    MofNCompleteColumn
)
from rich.status import Status
from rich.table import Table


class ConsoleUI:
    _console: Console
    _status: Status
    _spinner_type = 'clock'

    _complete_color = "[bold green]"
    _progress_color = "[bold cyan]"
    _print_color = "[bold green]"
    _rule_color = "[bold orange]"

    def __init__(self):
        self._console = Console()

    def start_loading(self, content: str):
        self._status = self._console.status(f"{self._progress_color}{content}...", spinner=self._spinner_type)
        self._status.start()

    def end_loading(self, content: str = ''):
        self._status.stop()
        self._console.print(f"{self._complete_color}{content}")
        del self._status

    _progress: Progress = None
    _tasks: dict[str, Task] = {}
    _progress_style = (
        SpinnerColumn('clock'),
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        'Прошло времени:',
        TimeElapsedColumn(),
        '|',
        MofNCompleteColumn(),
    )

    def start_progress(self, name: str, content: str, amount: int):
        if not self._progress:
            self._progress = Progress(*self._progress_style, expand=True)
            self._console = self._progress.console
        id_task = self._progress.add_task(f"{self._progress_color}{content}", total=amount)
        self._tasks[name] = self._progress.tasks[id_task]
        self._progress.start()

    def progress_stop(self, content: str = ''):
        self._progress.stop()
        self._console = Console()
        self._progress = None
        self._console.print(f"{self._complete_color}{content}")

    def progress_advance(self, name: str, advance: int):
        self._progress.advance(self._tasks[name].id, advance=advance)
        if not self._progress.finished and self._tasks[name].finished:
            self._progress.remove_task(self._tasks[name].id)
            del self._tasks[name]
        if self._progress.finished:
            self.progress_stop()

    def print(self, content: str):
        self._console.print(f"{self._print_color}{content}")

    def rule(self, content: str):
        self._console.rule(f"{self._rule_color}{content}")

    def simple_table(self, title: str, columns: list[str], rows: dict[str, any]):
        table = Table(title=f"{self._print_color}{title}")

        for col in columns:
            table.add_column(col)

        for key, value in rows.items():
            try:
                table.add_row(key, *value)
            except TypeError:
                table.add_row(key, str(value))
        self._console.print(table, justify='left')

class LoadingContext:
    _ui_item: ConsoleUI
    _display_text: str
    _complete_text: str

    def __init__(self, display_text: str, complete_text: str, console_ui: ConsoleUI):
        self._ui_item = console_ui
        self._display_text = display_text
        self._complete_text = complete_text

    def __enter__(self):
        self._ui_item.start_loading(self._display_text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ui_item.end_loading(self._complete_text)
