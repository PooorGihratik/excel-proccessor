from excel_processor import ProcessorUI, ConsoleUI

console_ui = ConsoleUI()
processor = ProcessorUI()
processor.set_ui(console_ui)
console_ui.display_welcome_text()

# try:
processor.process_files('TestFiles')


