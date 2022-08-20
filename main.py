from excel_processor import ProcessorUI, ConsoleUI, load_settings

settings = load_settings("Настройки.txt")

dev_mode = settings['debug_mode']
if dev_mode == 'true':
    console_ui = ConsoleUI()
    processor = ProcessorUI()
    processor.load_options(settings)
    processor.set_ui(console_ui)
    console_ui.display_welcome_text()
    processor.process_files()
else:
    console_ui = ConsoleUI()
    try:
        processor = ProcessorUI()
        processor.set_ui(console_ui)
        console_ui.display_welcome_text()
        processor.process_files()
    except:
        console_ui.print(f"[bold red]Произошла неизвестная ошибка. Процесс выполнения приостановлен")
input("Нажми enter чтобы выйти")
