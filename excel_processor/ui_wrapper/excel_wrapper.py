from .ui_wrapper import UIWrapper, LoadingContext
from ..core import PaymentSection
from typing import TextIO


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

    # Tables
    # ------------------------------------
    def final_sum(self, sums: dict[str, float]):
        self.ui_item.simple_table(f"Итоговые суммы (по счетам)", ["Счет", "Сумма"], sums)

    # Prints
    # ------------------------------------
    def payment_section_progress(self, section: PaymentSection):
        pass

    def text_file_print(self, file: TextIO, account: str, sections: list[PaymentSection]):
        count = len([info for section in sections for info in section.payment_items])

        result_str = ''
        if count % 100 in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
            result_str = f'Найдено {count} платежей'
        elif count % 10 == 1:
            if count == 1:
                result_str = f'Найден {count} платеж'
            else:
                result_str = f'Найдено {count} платеж'
        elif count % 10 in [2, 3, 4]:
            result_str = f'Найдено {count} платежа'
        elif count % 10 in [0, 5, 6, 7, 8, 9]:
            result_str = f'Найдено {count} платежей'

        self.ui_item.normal_print(f"[green]Файл [bold]{file.name}[/bold] загружен:")
        self.ui_item.normal_print(f"[magenta]{result_str} на счет {account}")

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
