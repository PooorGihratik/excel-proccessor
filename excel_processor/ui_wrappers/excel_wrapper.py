from .ui_wrapper import UIWrapper, LoadingContext
from ..core import PaymentSection


class UIExcelWrapper(UIWrapper):

    # Rules
    # ------------------------------------
    def status_load_workbooks(self):
        self.ui_item.rule("Инициализация книг")

    def status_load_files(self):
        self.ui_item.rule("Загрузка файлов")

    def status_distribute_payments(self):
        self.ui_item.rule("Разнесение платежей")

    def status_save_workbook(self):
        self.ui_item.rule("Сохранение книг")

    # Progress
    # ------------------------------------
    _payment_process_name = "PAYMENT_PROCESS"

    def payment_start_progress(self, data: dict[str, list[PaymentSection]]):
        count = len([info for account in data.values() for section in account for info in section.payment_items])
        self.ui_item.start_progress(
            self._payment_process_name,
            "Разнесение платежей...",
            count
        )

    def payment_process_advance(self):
        self.ui_item.progress_advance(self._payment_process_name, 1)

    def payment_advance(self):
        pass

    # Tables
    # ------------------------------------
    def final_sum(self, sums: dict[str, float]):
        self.ui_item.simple_table(f"Итоговые суммы (по счетам)", ["Счет", "Сумма"], sums)

    # Prints
    # ------------------------------------
    def payment_section_progress(self, section: PaymentSection):
        pass

    def done_print(self):
        self.ui_item.rule("Готово!")

    def error_print(self):
        self.ui_item.error("Произошла неизвестная ошибка. Выполнение программы прекращено.")

    # Statuses
    # ------------------------------------
    def loading_overall(self, name) -> LoadingContext:
        return LoadingContext(
            f"Загрузка файла \"{name}\"",
            f"Файл \"{name}\" загружен.",
            self.ui_item
        )

    def create_output_workbook(self, name) -> LoadingContext:
        return LoadingContext(
            f"Создание файла \"{name}\"",
            f"Файл \"{name}\" создан.",
            self.ui_item
        )

    def save_book(self, name: str) -> LoadingContext:
        return LoadingContext(
            f"Сохранение \"{name}\"",
            f"Файл \"{name}\" сохранен.",
            self.ui_item
        )
