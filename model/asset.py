import re
from common import constants as const
from model.asset_types import AssetTypes, build_asset_type_from_string


class Asset:
    def __init__(self, id: int, name: AssetTypes, value: str):
        self.id = id
        self.type: AssetTypes = name
        self.value = value

    def __str__(self):
        return f"{self.id}. {self.type}: {self.value}"


def _build_none_error(field: str):
    f"""{field} is None"""


null_object = Asset(-1, const.EMPTY_FIELD, const.EMPTY_FIELD)


def parse_from_str(s: str) -> (Asset, str):
    id_match = re.search(r"\d+(?=\.)", s)
    if not id_match:
        return null_object, _build_none_error("id")
    name_match = re.search(r"(?<=\d\.)\s*\w+\s*(?=:\s*\d+)", s)
    if not name_match:
        return null_object, _build_none_error("name")
    value_match = re.search(r"(?<=:)\s*\d+", s)

    if not value_match:
        return null_object, _build_none_error("value")
    id_str = id_match.group()

    if not id_str.isdigit():
        return null_object, "id is not a digit"
    type = build_asset_type_from_string(name_match.group().strip())

    if type is AssetTypes.UNKNOWN:
        return null_object, "unknown asset type"

    id = int(id_str.strip())
    value = value_match.group().strip()

    return Asset(id, type, value), const.EMPTY_FIELD
