from .payment_file_parser import PaymentFileParser
from .payment_workbook_register import PaymentWorkbookRegister
from .common import PaymentSection
from .payment_sheet_generator import PaymentSheetGenerator
from openpyxl import Workbook, load_workbook
from dataclasses import dataclass


@dataclass
class SheetRegisterOption:
    account: str
    target_sheet_index: int
    payments_sheet_index: int
    dept_sheet_index: int


@dataclass
class ProcessorOptions:
    file_extension: str
    overall_file_name: str
    output_file_name: str
    sheets: list[SheetRegisterOption]


class ExcelPaymentProcessor:
    _config = ProcessorOptions(
        output_file_name='расшифровка банка',
        overall_file_name='Overall',
        file_extension='.xlsx',
        sheets=[
            # Utility
            SheetRegisterOption(
                account="40703810211180030006",
                target_sheet_index=0,
                payments_sheet_index=1,
                dept_sheet_index=3
            ),
            # Overhaul
            SheetRegisterOption(
                account="40705810011000000589",
                target_sheet_index=4,
                payments_sheet_index=5,
                dept_sheet_index=7
            ),
        ],
    )

    def __init__(self, config: ProcessorOptions = None):
        if config is not None:
            self.load_options(config)

    def load_options(self, config: ProcessorOptions):
        self._config = config
    
    _overall_read_workbook: Workbook
    _overall_write_workbook: Workbook
    _generated_workbook: Workbook
    _payment_sheet_generator = PaymentSheetGenerator()
    _registerer_dict: dict[str, PaymentWorkbookRegister] = {}
    _count = 0

    def is_workbooks_loaded(self):
        return self._overall_read_workbook and self._overall_write_workbook and self._generated_workbook
    
    def load_workbooks(self):
        self._overall_read_workbook = load_workbook(
            filename=self._config.overall_file_name + self._config.file_extension,
            data_only=True,
            read_only=True
        )
        
        self._overall_write_workbook = load_workbook(
            filename=self._config.overall_file_name + self._config.file_extension
        )

        for sheet_params in self._config.sheets:
            self._registerer_dict[sheet_params.account] = PaymentWorkbookRegister(
                self._overall_read_workbook.worksheets[sheet_params.target_sheet_index],
                self._overall_write_workbook.worksheets[sheet_params.payments_sheet_index],
                self._overall_write_workbook.worksheets[sheet_params.dept_sheet_index]
            )

        self._generated_workbook = Workbook()
        self._generated_workbook.remove(self._generated_workbook.worksheets[0])
        self._payment_sheet_generator.workbook = self._generated_workbook

    def close_workbooks(self):
        self._overall_read_workbook.close()
        self._overall_write_workbook.close()
        self._generated_workbook.close()

        self._payment_sheet_generator.workbook = None
        self._registerer_dict = {}

    def save_workbooks(self):
        self._generated_workbook.save(filename=self._config.output_file_name + self._config.file_extension)
        self._overall_write_workbook.save(filename=self._config.overall_file_name + self._config.file_extension)

    def register_sections(self, payments_sections: list[PaymentSection]):
        if not self.is_workbooks_loaded():
            self.load_workbooks()

        for section in payments_sections:
            registerer = self._registerer_dict[section.account]
            if registerer:
                for payment in section.payment_items:
                    # TODO: make an dept direction
                    if payment.period.year == 22: 
                        registerer.add_payment(payment)
            self._payment_sheet_generator.add_payment_section(section)

    def process_files(self, directory: str):
        file_parser = PaymentFileParser(directory)
        self.load_workbooks()
        payment_data = file_parser.parse_all_files_in_directory()
        sum_payments = {}
        for key in payment_data.keys():
            sum_payments[key] = 0
        for item in payment_data.values():
            for section in item:
                for info in section.payment_items:
                    sum_payments[section.account] += info.payment
            self.register_sections(item)
        print(sum_payments)
        self.save_workbooks()
        self.close_workbooks()
        
