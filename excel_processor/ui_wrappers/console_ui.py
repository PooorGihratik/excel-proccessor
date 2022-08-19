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


class ConsoleUI:
    _console: Console
    _status: Status
    _spinner_type = 'clock'

    _progress: Progress
    _tasks: dict[str, Task]
    _process_style = (
        SpinnerColumn('clock'),
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        'Прошло времени:',
        TimeElapsedColumn(),
        '|',
        MofNCompleteColumn(),
    )

    _complete_color = "[bold green]"
    _progress_color = "[bold cyan]"
    _print_color = "[bold green]"

    def __init__(self):
        self._console = Console()

    def start_loading(self, content: str):
        self._status = self._console.status(f"{self._progress_color}{content}...", spinner=self._spinner_type)
        self._status.start()

    def end_loading(self, content: str = ''):
        self._status.stop()
        self._console.print(f"{self._complete_color}{content}")
        del self._status

    def start_progress(self, name: str, content: str, amount: int):
        if not self._progress:
            self._progress = Progress(*self._process_style, expand=True)
            self._console = self._progress.console
        id_task = self._progress.add_task(f"{self._progress_color}{content}", total=amount)
        self._tasks[name] = self._progress.tasks[id_task]
        self._progress.start()

    def progress_stop(self, content: str = ''):
        self._progress.stop()
        self._console = Console()
        del self._progress
        self._console.print(f"{self._complete_color}{content}")

    def progress_advance(self, name: str, advance: int):
        self._progress.advance(self._tasks[name].id, advance=advance)
        if self._progress.finished:
            self.progress_stop()
        if self._tasks[name].finished:
            self._progress.remove_task(self._tasks[name].id)
            del self._tasks[name]

    def print(self, content: str):
        self._console.print(content)

    def rule(self, content: str):
        self._console.rule(content)
