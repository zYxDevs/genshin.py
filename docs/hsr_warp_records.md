# HSR Warp Records Statistics

This is a HoYoLAB feature that shows statistics of a player's warps: recently obtained 5-star items, per-banner warp counts, and the 5-star items obtained from each banner type along with the current pity.

Cookies are required. The API additionally needs an `e_hkrpg_token` cookie which the client obtains automatically; when the account's cookie token has expired, an `stoken` cookie is required to mint a new one.

## Example

```py
import genshin

client = genshin.Client(cookies, uid=809162009, lang="en-us")  # (1)

brief = await client.get_starrail_warp_brief()  # (2)
for entry in brief.items:
    print(f"{entry.item.name} x{entry.count}")

pool_stats = await client.get_starrail_warp_pool_stats(genshin.models.StarRailBannerType.CHARACTER)  # (3)
for pool in pool_stats:
    print(f"{pool.name} ({pool.version}): {pool.total_count} warps, {pool.up_count}x {pool.up_item.name}")

five_stars = await client.get_starrail_five_star_warps(genshin.models.StarRailBannerType.CHARACTER)  # (4)
print(f"Current pity: {five_stars.pity}")
for warp in five_stars.warps:
    print(f"{warp.item.name} in {warp.count} warps ({'rate-up' if warp.is_up else 'lost 50/50'})")
```

1. The `lang` parameter controls the language of item and banner names.
2. The most recently obtained 5-star items across all banners.
3. Statistics of every banner of the given type the player has warped on.
4. All pages are fetched, so this returns every 5-star item ever obtained from the given banner type.
