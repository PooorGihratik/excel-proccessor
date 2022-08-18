import datetime
from dataclasses import dataclass


@dataclass
class Period:
    initial: str
    month: int
    year: int


@dataclass
class PaymentInfo:
    date: datetime
    apartment: int
    fullname: str
    period: Period
    full_payment: float
    payment: float
    percent: float


@dataclass
class PaymentSection:
    account: str
    header_items: list[str]
    payment_items: list[PaymentInfo]


def get_account_key(name):
    return name.split('_')[-2]


def convert_str_to_date(string: str):
    date = string.split('-')
    return datetime.datetime(int(date[2]), int(date[1]), int(date[0]))


def get_period(string: str):
    return Period(
        initial=string,
        month=int(string[:-2]),
        year=int(string[-2:])
    )
