from excel_processor import ProcessorUI, ConsoleUI

dev_mode = False

if dev_mode:
    console_ui = ConsoleUI()
    processor = ProcessorUI()
    processor.set_ui(console_ui)
    console_ui.display_welcome_text()
    processor.process_files('TestFiles')
else:
    console_ui = ConsoleUI()
    try:
        processor = ProcessorUI()
        processor.set_ui(console_ui)
        console_ui.display_welcome_text()
        processor.process_files('TestFiles')
    except:
        console_ui.print(f"[bold red]Произошла неизвестная ошибка. Процесс выполнения приостановлен")
