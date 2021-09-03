from typing import Any, List

from repository import savings as repo
from model import saving as m


class SavingsSv:

    def __init__(self, savings_repo: repo.SavingsRepo):
        self._repo = savings_repo

    def fetch_all(self) -> List[m.Saving]:
        rows: List[Any] = self._repo.fetch_all()
        return list(map(lambda r: m.Saving(r[0], r[1], r[2]), rows))

    def update(self, asset: m.Saving) -> None:
        self._repo.upd(asset.id, asset)

savings_sv_instance = SavingsSv(repo.saving_repo_instance)
