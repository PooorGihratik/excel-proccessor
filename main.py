# Секция кода
# ------------------------------------------
from excel_processor import ExcelPaymentProcessor

processor = ExcelPaymentProcessor()
processor.process_files('Files')
print("Готово!")
input("Нажми enter, чтобы закрыть консоль ;)")

# Старый код (не работает)
# ------------------------------------------
# Директория, в которой будет проиходить поиск файлов
# directory = "Files"

# Имя книги, в которую будут заноситься данные об оплате
# name_of_overall = "Overall"

# Get all file names
# files = list((Path('.') / directory).glob('*.txt'))
#
# print(files)
#
# # Finding all accounts
# print("\nСоздание книг...")
# workbookDictionary = {}
# min_length = 0
#
#
# for file_name in files:
#     workbookKey = AccountSheet.get_account_key(file_name.name)
#     if len(file_name.name) > min_length:
#         min_length = len(file_name.name)
#     if workbookKey not in workbookDictionary.keys():
#         workbookDictionary[workbookKey] = AccountSheet(workbookKey, overall)
#
# print("Запись данных файлов в таблицы...")
# print("---------------------")
# for file_path in files:
#     workbook = workbookDictionary[AccountSheet.get_account_key(file_path.name)]
#     file = file_path.open(mode='r', encoding="windows-1251")
#     lines = file.readlines()
#     workbook.add_file_data(lines)
#     print(file_path.name + (min_length - len(file_path.name)) * ' ', " > ", workbook.get_file_name())
# print("---------------------\n")
# print("Сохранение книг...")
# print("---------------------")
# for workbook in workbookDictionary.values():
#     print(workbook.get_file_name())
#     workbook.save_sheet()
#
# print("Сохранение " + name_of_overall + "...")
# overall.save_book()
# print("---------------------\n")


