from .ui_wrapper import UIExcelWrapper, UIWrapable
from .core import (
    PaymentFileParser,
    ProcessorOptions,
    PaymentWorkbookRegister,
    PaymentInfo,
    PaymentSection
)


class ProcessorUI(UIWrapable):
    _payment_processor = PaymentWorkbookRegister()
    _directory: str = 'Files'

    _options_map = {
        "year": "year",
        "overall_book": "overall_file_name",
        "bank_parse": "output_file_name",
    }

    def __init__(self, config: ProcessorOptions = None):
        super().__init__(UIExcelWrapper)
        if config is not None:
            self._payment_processor.load_options(config)

    def load_options(self, options: dict[str, str]):
        config = self._payment_processor.get_options()
        for key, value in options.items():
            if value == 'auto':
                continue
            else:
                if key == "directory":
                    self._directory = key
                elif key in self._options_map.keys():
                    config.__setattr__(self._options_map[key], value)
        self._payment_processor.load_options(config)

    def info_process_callback(self, info: PaymentInfo):
        self._ui_wrapper.payment_process_advance()

    def section_callback(self, section: PaymentSection):
        pass

    def process_files(self):
        directory = self._directory
        self._ui_wrapper.status_load_workbooks()
        with self._ui_wrapper.create_output_workbook(self._payment_processor.bank_workbook_name):
            self._payment_processor.create_bank_workbook()
        with self._ui_wrapper.loading_overall(self._payment_processor.overall_book_name) as context:
            try:
                self._payment_processor.load_overall()
            except FileNotFoundError:
                context.complete_text =\
                    f"Файл \"{self._payment_processor.overall_book_name}\" не найден. " \
                    f"Выплаты не будут зарегистрированны в книге"

        self._ui_wrapper.status_load_files()
        file_parser = PaymentFileParser(directory)
        payment_data = file_parser.parse_all_files_in_directory(
            file_callback=self._ui_wrapper.text_file_print
        )

        if len(payment_data.items()) != 0:
            self._ui_wrapper.status_distribute_payments()
            self._ui_wrapper.payment_start_progress(payment_data)
            sum_payments = self._payment_processor.distribute_payments(
                payment_data,
                info_callback=self.info_process_callback,
                section_callback=self.section_callback
            )
            self._ui_wrapper.final_sum(sum_payments)

            self._ui_wrapper.status_save_workbook()
            with self._ui_wrapper.save_book(self._payment_processor.bank_workbook_name):
                self._payment_processor.save_bank_workbook()
                self._payment_processor.close_bank_workbook()
            if self._payment_processor.is_overall_loaded:
                with self._ui_wrapper.save_book(self._payment_processor.overall_output_book_name):
                    self._payment_processor.save_overall()
                    self._payment_processor.close_overall()

        else:
            self._ui_wrapper.no_payments()
            self._payment_processor.close_bank_workbook()
            if self._payment_processor.is_overall_loaded:
                self._payment_processor.close_overall()

        self._ui_wrapper.done_print()
