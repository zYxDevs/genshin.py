"""Starrail Chronicle Base Model."""

import datetime
import typing

from genshin.models.model import APIModel


class PartialTime(APIModel):
    """Partial time model."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    tzinfo: typing.Optional[int] = None
    """UTC offset of the account's server in hours, if known."""

    @property
    def datetime(self) -> datetime.datetime:
        tz = datetime.timezone(datetime.timedelta(hours=self.tzinfo)) if self.tzinfo is not None else None
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, tzinfo=tz)
