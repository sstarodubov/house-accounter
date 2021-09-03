from typing import Any, List

from repository import assets as repo
from model import asset as m


class AssetsSv:

    def __init__(self, asset_repo: repo.AssetRepo):
        self._repo = asset_repo

    def fetch_all(self) -> List[m.Asset]:
        rows: List[Any] = self._repo.fetch_all()
        return list(map(lambda r: m.Asset(r[0], r[1], r[2]), rows))

    def update(self, asset: m.Asset) -> None:
        self._repo.upd(asset.id, asset)


asset_sv_instance = AssetsSv(repo.asset_repo_instance)
