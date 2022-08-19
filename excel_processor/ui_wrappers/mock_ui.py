class MockUI:
    def start_loading(self, content: str):
        pass

    def end_loading(self, content: str = ''):
        pass

    def start_progress(self, name: str, content: str, amount: int):
        pass

    def progress_stop(self, content: str = ''):
        pass

    def progress_advance(self, name: str, advance: int):
        pass

    def print(self, content: str):
        pass

    def rule(self, content: str):
        pass

    def simple_table(self, title: str, columns: list[str], rows: dict[str, any]):
        pass
