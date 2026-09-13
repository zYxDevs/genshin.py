"""HSR warp records statistics component."""

import typing

from genshin import types, utility
from genshin.client import routes
from genshin.client.components import badge
from genshin.models.genshin import gacha as gacha_models
from genshin.models.starrail import warp_records as models

__all__ = ("HSRWarpRecordsClient",)

GACHA_TYPES: typing.Mapping[gacha_models.StarRailBannerType, str] = {
    gacha_models.StarRailBannerType.STANDARD: "GachaType_Standard",
    gacha_models.StarRailBannerType.NOVICE: "GachaType_Newbie",
    gacha_models.StarRailBannerType.CHARACTER: "GachaType_AvatarUp",
    gacha_models.StarRailBannerType.WEAPON: "GachaType_EquipmentUp",
    gacha_models.StarRailBannerType.FATE_CHARACTER: "GachaType_CollabAvatarUp",
    gacha_models.StarRailBannerType.FATE_WEAPON: "GachaType_CollabEquipmentUp",
}
"""Mapping of banner types to the ``gacha_type`` values used by the warp records API."""


class HSRWarpRecordsClient(badge.BadgeLoginClient):
    """HSR warp records statistics client."""

    async def _request_warp_records(
        self,
        endpoint: str,
        uid: typing.Optional[int] = None,
        *,
        lang: typing.Optional[str] = None,
        params: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> typing.Mapping[str, typing.Any]:
        """Make a request towards the warp records API."""
        uid = uid or await self._get_uid(types.Game.STARRAIL)
        region = utility.recognize_region(uid, game=types.Game.STARRAIL) or types.Region.OVERSEAS
        params = {
            "game_biz": utility.get_prod_game_biz(region, types.Game.STARRAIL),
            "region": utility.recognize_starrail_server(uid),
            "uid": uid,
            **(params or {}),
        }
        url = routes.HKRPG_GACHA_RECORD_URL.get_url(region) / endpoint
        return await self._request_with_badge(types.Game.STARRAIL, url, uid, lang=lang, params=params)

    async def get_starrail_warp_brief(
        self,
        uid: typing.Optional[int] = None,
        *,
        lang: typing.Optional[str] = None,
    ) -> models.StarRailWarpBrief:
        """Get an overview of the most recently obtained 5-star items across all banners."""
        data = await self._request_warp_records("brief", uid, lang=lang)
        return models.StarRailWarpBrief(**data)

    async def get_starrail_warp_pool_stats(
        self,
        banner_type: gacha_models.StarRailBannerType,
        uid: typing.Optional[int] = None,
        *,
        lang: typing.Optional[str] = None,
    ) -> typing.Sequence[models.StarRailWarpPoolStat]:
        """Get per-banner warp statistics for a banner type."""
        gacha_type = GACHA_TYPES[gacha_models.StarRailBannerType(banner_type)]
        data = await self._request_warp_records("pool_stat", uid, lang=lang, params={"gacha_type": gacha_type})
        return [models.StarRailWarpPoolStat(**card) for card in data["cards"]]

    async def get_starrail_five_star_warps(
        self,
        banner_type: gacha_models.StarRailBannerType,
        uid: typing.Optional[int] = None,
        *,
        lang: typing.Optional[str] = None,
    ) -> models.StarRailFiveStarWarps:
        """Get all 5-star items obtained from a banner type along with the current pity."""
        params: typing.Dict[str, typing.Any] = {"gacha_type": GACHA_TYPES[gacha_models.StarRailBannerType(banner_type)]}

        rows: typing.List[typing.Mapping[str, typing.Any]] = []
        while True:
            data = await self._request_warp_records("five_star_list", uid, lang=lang, params=params)
            rows.extend(data["list"])
            if not data["has_more"]:
                break
            params = {**params, "version_id": data["version_id"], "max_id": data["next_max_id"]}

        # The row without an item is the ongoing streak towards the next 5-star.
        pity = next((row["gacha_count"] for row in rows if not row["got_item"]), 0)
        warps = [models.StarRailFiveStarWarp(**row) for row in rows if row["got_item"]]
        return models.StarRailFiveStarWarps(version_id=data["version_id"], pity=pity, warps=warps)
