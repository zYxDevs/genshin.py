from typing import Any, Mapping, Optional, Sequence

from pydantic import field_validator

from genshin import types
from genshin.models.model import Aliased, APIModel, UnixDateTime

__all__ = (
    "AccompanyCharacter",
    "AccompanyCharacterAttribute",
    "AccompanyCharacterDetails",
    "AccompanyCharacterGame",
    "AccompanyCharacterInfo",
    "AccompanyCharacterProfile",
    "AccompanyInfo",
    "AccompanyResult",
    "AccompanyVoiceLine",
    "AccompanyVoiceSetting",
    "AccompanyWikiImage",
    "AccompanyWikiVideo",
)


class AccompanyCharacterInfo(APIModel):
    """Accompany character info."""

    role_id: int
    game_id: int
    name: str
    brief_name: str
    topic_id: int
    game_name: str


class AccompanyCharacterProfile(APIModel):
    """Accompany character color and images."""

    card_color: str
    bg_dark_color: str
    bg_light_color: str
    bg_card_color: str

    card_image: str = Aliased("card_img_url")
    video: str = Aliased("full_screen_video_265")
    icon: str = Aliased("icon_url")


class AccompanyCharacter(APIModel):
    """Accompany character."""

    info: AccompanyCharacterInfo = Aliased("basic")
    profile: AccompanyCharacterProfile = Aliased("attr_profile")
    attribute_ids: Sequence[int]


class AccompanyCharacterAttribute(APIModel):
    """Accompany character attribute."""

    id: int
    icon: str = Aliased("icon_url")
    corner_icon: str = Aliased("corner_icon_url")


class AccompanyCharacterGame(APIModel):
    """Accompany character game."""

    attributes: Sequence[Sequence[AccompanyCharacterAttribute]] = Aliased("attribute_group_list")
    id: int = Aliased("game_id")
    icon: str = Aliased("game_icon")
    characters: Sequence[AccompanyCharacter] = Aliased("role_list")

    @field_validator("attributes", mode="before")
    def __unnest_attributes(cls, v: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
        return [group["attribute_list"] for group in v]

    @property
    def game(self) -> types.Game:
        if self.id == 2:
            return types.Game.GENSHIN
        if self.id == 6:
            return types.Game.STARRAIL
        if self.id == 8:
            return types.Game.ZZZ

        raise ValueError(f"Unknown game ID: {self.id}")


class AccompanyResult(APIModel):
    """Accompany result."""

    accompany_days: int
    points_increased: int = Aliased("increase_accompany_point")


class AccompanyInfo(APIModel):
    """Accompany progress of a character."""

    days: int = Aliased("accompany_days")
    quarter_days: int = Aliased("accompany_quarter_days")
    accompanied_today: bool = Aliased("is_accompany_today")
    can_accompany: bool
    points: int = Aliased("accompany_point")
    available_points: int = Aliased("available_accompany_point")


class AccompanyVoiceLine(APIModel):
    """Accompany character voice line."""

    voice_url: str = Aliased("voice")
    text: str = Aliased("script")


class AccompanyWikiVideo(APIModel):
    """Accompany character wiki video."""

    video_id: str
    video_url: str
    cover_url: str
    synced_at: UnixDateTime = Aliased("sync_unix")
    sort: int


class AccompanyWikiImage(APIModel):
    """Accompany character wiki gallery image."""

    image_url: str
    origin_url: str
    height: int
    width: int
    size: int
    synced_at: UnixDateTime = Aliased("sync_unix")


class AccompanyCharacterDetails(APIModel):
    """Accompany character page details."""

    info: AccompanyCharacterInfo = Aliased("basic")
    profile: AccompanyCharacterProfile = Aliased("attr_profile")
    accompany_info: AccompanyInfo
    voice_scripts: Mapping[str, Sequence[AccompanyVoiceLine]] = Aliased("attr_wiki_voice_script")
    videos: Sequence[AccompanyWikiVideo] = Aliased("attr_wiki_video")
    gallery: Sequence[AccompanyWikiImage] = Aliased("attr_wiki_gallery")

    @field_validator("voice_scripts", mode="before")
    def __unnest_voice_scripts(cls, v: Optional[dict[str, Any]]) -> dict[str, Any]:
        return {name: script["list"] for name, script in v["scripts"].items()} if v else {}

    @field_validator("videos", mode="before")
    def __unnest_videos(cls, v: Optional[dict[str, Any]]) -> list[Any]:
        return v["videos"] if v else []

    @field_validator("gallery", mode="before")
    def __unnest_gallery(cls, v: Optional[dict[str, Any]]) -> list[Any]:
        return v["images"] if v else []


class AccompanyVoiceSetting(APIModel):
    """Voice and subtitle language setting of an accompany character."""

    voice_lang: str
    script_lang: str
    updated_at: UnixDateTime = Aliased("setting_unix")
