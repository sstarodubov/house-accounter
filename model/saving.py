import re
from common import constants as const


class Saving:
    def __init__(self, id: int, name: str, value: str):
        self.id = id
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.id}. {self.name}: {self.value}"


def _build_none_error(field: str):
    f"""{field} is None"""


null_object = Saving(-1, const.EMPTY_FIELD, const.EMPTY_FIELD)


def parse_from_str(s: str) -> (Saving, str):
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
    id = int(id_str.strip())
    name = name_match.group().strip()
    value = value_match.group().strip()
    return Saving(id, name, value), const.EMPTY_FIELD
