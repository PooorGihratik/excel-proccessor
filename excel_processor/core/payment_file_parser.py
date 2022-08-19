from .common import (
    get_period,
    get_account_key,
    convert_str_to_date,
    PaymentInfo,
    PaymentSection
)
from pathlib import Path


class PaymentFileParser:
    target_directory = ''

    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def get_file_names(self) -> list[str]:
        return [item.name for item in list((Path('../..') / self.target_directory).glob('*.txt'))]

    def get_account_names(self) -> list[str]:
        return [get_account_key(item) for item in self.get_file_names()]

    def parse_all_files_in_directory(self) -> dict[str, list[PaymentSection]]:
        files_dict = {}
       
        for file_name in self.get_account_names():
            files_dict[file_name] = []

        files = list((Path('./.') / self.target_directory).glob('*.txt'))
        for file_path in files:
            file = file_path.open(mode='r', encoding="windows-1251")
            lines = file.readlines()
            section_item = PaymentSection(
                account=get_account_key(file_path.name),
                header_items=lines[-1].replace(u'\xa0', '').replace('\n', '').replace('=', '').split(';'),
                payment_items=[]
            )
            lines.pop()

            # Content
            for line in lines:
                line_items = line.replace(u'\xa0', '').split(';')
                section_item.payment_items.append(PaymentInfo(
                    date=convert_str_to_date(line_items[0]),
                    apartment=int(line_items[5]),
                    fullname=line_items[6],
                    period=get_period(line_items[8]),
                    full_payment=float(line_items[9].replace(',', '.')),
                    payment=float(line_items[10].replace(',', '.')),
                    percent=float(line_items[11].replace(',', '.'))
                ))
            if get_account_key(file_path.name) not in files_dict:
                files_dict[get_account_key(file_path.name)] = []
            files_dict[get_account_key(file_path.name)].append(section_item)
            file.close()
        return files_dict
