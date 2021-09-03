from typing import Dict

import requests
from common import constants as const


class ExchangerSv:
    def __init__(self):
        self.secret_key: str = _get_secret_key()

    def fetch_course_based_by_eur(self) -> (Dict[str, str], str):
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key={self.secret_key}"

        response = requests.get(url)
        if response.status_code != 200:
            return const.EMPTY_FIELD, f"api.exchangeratesapi.io responded: {response.text}"
        json = response.json()
        courses = {
            "EUR": 1.00,
            "USD": json["rates"]["USD"],
            "RUR": json["rates"]["RUB"]
        }
        return courses, const.EMPTY_FIELD


def _get_secret_key() -> str:
    with open("secret_key_exchanger.txt", "r") as file:
        return file.readline()


exchanger_sv_instance = ExchangerSv()

exchanger_sv_instance.fetch_course_based_by_eur()
