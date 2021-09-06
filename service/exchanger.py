import time
from typing import Dict

import requests
from common import constants as const
from repository import exchanger as ex_repo


class ExchangerSv:
    def __init__(self, exchanger_repo: ex_repo.ExchangerRepo):
        self._secret_fiat_key: str = _get_exchanger_secret_key()
        self._secret_etherscan_key: str = _get_etherscan_secret_key()
        self._exchanger_repo = exchanger_repo

    def _fetch_ether_price(self) -> (float, str):
        url = f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={self._secret_etherscan_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return -1, f"etherscan responded: {response.text}"
        json = response.json()
        cur_price = json["result"]["ethusd"]
        return cur_price, const.EMPTY_FIELD

    def _fetch_fiat_rates_outside(self) -> (Dict[str, float], str):
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key={self._secret_fiat_key}"

        response = requests.get(url)
        if response.status_code != 200:
            return {}, f"api.exchangeratesapi.io responded: {response.text}"
        json = response.json()
        rates = {
            "EUR_IN_EUR": 1.00,
            "RUR_IN_RUR": 1.00,
            "USD_IN_EUR": json["rates"]["USD"],
            "RUR_IN_EUR": json["rates"]["RUB"]
        }
        self._compute_usd(rates)
        return rates, const.EMPTY_FIELD

    def fetch_rates(self) -> (Dict[str, float], str):
        cur_rate, last_time_update = self._exchanger_repo.fetch_rates()
        cur_eth_price_in_usd, eth_err = self._fetch_ether_price()
        if eth_err != const.EMPTY_FIELD:
            return {}, eth_err
        cur_time = time.time()
        if cur_time - last_time_update < 43200000:
            return (cur_rate | {"RUR_IN_RUR": 1.0, "RUR_IN_ETH": float(cur_eth_price_in_usd) * cur_rate["RUR_IN_USD"]}
                    , const.EMPTY_FIELD)
        rates, fiat_err = self._fetch_fiat_rates_outside()
        if fiat_err != const.EMPTY_FIELD:
            return {}, fiat_err
        return rates | {"USD_IN_ETH": float(cur_eth_price_in_usd) * rates["RUR_IN_USD"]}, const.EMPTY_FIELD

    @staticmethod
    def _compute_usd(m: Dict[str, float]):
        rur_in_usd = m["RUR_IN_EUR"] / m["USD_IN_EUR"]
        m["RUR_IN_USD"] = rur_in_usd

    def update_rates(self) -> str:
        cur_rate, last_time_update = self._exchanger_repo.fetch_rates()
        cur_time = time.time()
        if cur_time - last_time_update < 43200000:
            return const.EMPTY_FIELD
        rates, err = self._fetch_fiat_rates_outside()
        if err != const.EMPTY_FIELD:
            return err
        self._exchanger_repo.update_rate("USD", rates["RUR_IN_USD"])
        self._exchanger_repo.update_rate("EUR", rates["RUR_IN_EUR"])
        return const.EMPTY_FIELD


def _get_exchanger_secret_key() -> str:
    with open(const.SECRET_KEY_EXCHANGE_PATH, "r") as file:
        return file.readline()


def _get_etherscan_secret_key() -> str:
    with open(const.SECRET_KEY_ETHERSCAN_PATH, "r") as file:
        return file.readline()


exchanger_sv_instance = ExchangerSv(ex_repo.exchanger_repo_instance)
