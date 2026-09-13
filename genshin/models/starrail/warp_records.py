"""Star Rail warp records statistics models."""

import typing

from genshin.models.model import Aliased, APIModel, Unique

__all__ = (
    "StarRailFiveStarWarp",
    "StarRailFiveStarWarps",
    "StarRailWarpBrief",
    "StarRailWarpBriefItem",
    "StarRailWarpItem",
    "StarRailWarpPoolStat",
)


class StarRailWarpItem(APIModel, Unique):
    """Item obtained from a warp."""

    id: int = Aliased("item_id")
    name: str
    icon: str
    big_icon: str
    type: str = Aliased("item_type")
    rarity: int


class StarRailWarpBriefItem(APIModel):
    """Recently obtained 5-star item with its count."""

    item: StarRailWarpItem
    count: int


class StarRailWarpBrief(APIModel):
    """Overview of recently obtained 5-star items across all banners."""

    version_id: int
    items: typing.Sequence[StarRailWarpBriefItem]


class StarRailWarpPoolStat(APIModel):
    """Statistics of a single warp banner."""

    banner_id: int = Aliased("gacha_id")
    version: str
    name: str = Aliased("pool_name")
    total_count: int
    up_count: int
    up_item: typing.Optional[StarRailWarpItem] = None


class StarRailFiveStarWarp(APIModel, Unique):
    """A 5-star item obtained from a warp banner type."""

    id: int
    uuid: str
    item: StarRailWarpItem
    is_up: bool
    count: int = Aliased("gacha_count")
    """Amount of warps it took to obtain this item."""


class StarRailFiveStarWarps(APIModel):
    """All 5-star items obtained from a warp banner type."""

    version_id: int
    pity: int
    """Amount of warps since the last 5-star item."""
    warps: typing.Sequence[StarRailFiveStarWarp]
