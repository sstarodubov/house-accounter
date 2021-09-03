from enum import Enum


class AssetTypes(Enum):
    RUR = 0
    USD = 1
    EUR = 2
    ETH = 3
    BTC = 4
    GOLD = 5
    UNKNOWN = 6

    def __str__(self):
        if self is AssetTypes.BTC:
            return "BTC"
        if self is AssetTypes.RUR:
            return "RUR"
        if self is AssetTypes.EUR:
            return "EUR"
        if self is AssetTypes.USD:
            return "USD"
        if self is AssetTypes.GOLD:
            return "GOLD"
        if self is AssetTypes.ETH:
            return "ETH"
        raise Exception("unknown assert type")


def build_asset_type_from_string(s:str) -> AssetTypes:
    if s == AssetTypes.BTC.__str__():
        return AssetTypes.BTC
    if s == AssetTypes.RUR.__str__():
        return AssetTypes.RUR
    if s == AssetTypes.EUR.__str__():
        return AssetTypes.EUR
    if s == AssetTypes.USD.__str__():
        return AssetTypes.USD
    if s == AssetTypes.GOLD.__str__():
        return AssetTypes.GOLD
    if s == AssetTypes.ETH.__str__():
        return AssetTypes.ETH
    return AssetTypes.UNKNOWN
