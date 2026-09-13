import genshin


async def test_warp_brief(hsr_client: genshin.Client):
    brief = await hsr_client.get_starrail_warp_brief()
    assert brief.version_id
    assert all(item.item.rarity == 5 for item in brief.items)


async def test_warp_pool_stats(hsr_client: genshin.Client):
    stats = await hsr_client.get_starrail_warp_pool_stats(genshin.models.StarRailBannerType.CHARACTER)
    assert stats
    assert stats[0].up_item is not None


async def test_warp_pool_stats_standard(hsr_client: genshin.Client):
    stats = await hsr_client.get_starrail_warp_pool_stats(genshin.models.StarRailBannerType.STANDARD)
    assert stats
    assert stats[0].up_item is None


async def test_five_star_warps(hsr_client: genshin.Client):
    warps = await hsr_client.get_starrail_five_star_warps(genshin.models.StarRailBannerType.CHARACTER)
    assert warps.pity >= 0
    assert all(warp.item.rarity == 5 for warp in warps.warps)
