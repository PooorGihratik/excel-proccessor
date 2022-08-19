from excel_processor import ExcelPaymentProcessor, ConsoleUI

processor = ExcelPaymentProcessor()
processor.set_ui(ConsoleUI())
processor.process_files('TestFiles')
