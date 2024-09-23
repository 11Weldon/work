from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, PlainSerializer, ValidationInfo

OFStrStrMap = dict[str, str]
OFStrIntMap = dict[str, int]
OFIntIntMap = dict[int, int]

ZWOF_DT_SEC_FORMAT = "%Y-%b-%d %H:%M:%S"
ZWOF_DT_FORMAT = f"{ZWOF_DT_SEC_FORMAT}.%f"
ZWOF_TIME_ZONE = timezone.utc


def zwof_to_datetime(indatetime: str | datetime | None) -> datetime | None:
    if isinstance(indatetime, datetime):
        if indatetime.tzinfo != ZWOF_TIME_ZONE:
            return indatetime.astimezone(tz=ZWOF_TIME_ZONE)
        return indatetime

    if indatetime is None:
        return None

    if isinstance(indatetime, str):
        if "." not in indatetime:
            indatetime += ".0"

        return datetime.strptime(indatetime, ZWOF_DT_FORMAT).replace(tzinfo=ZWOF_TIME_ZONE)

    raise TypeError(f'Invalid type for input date {type(indatetime)}')


def datetime_to_zwof(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    dt_of = dt.astimezone(tz=ZWOF_TIME_ZONE)
    return dt_of.strftime(ZWOF_DT_FORMAT if dt_of.microsecond else ZWOF_DT_SEC_FORMAT)


OFdatetime = Annotated[
    datetime, BeforeValidator(zwof_to_datetime), PlainSerializer(datetime_to_zwof)
]

OFIntDtMap = dict[int, OFdatetime]
OFStrDtMap = dict[str, OFdatetime]


# Non fully documented


class IntResult(BaseModel):
    result: int


class StrResult(BaseModel):
    result: str


class BoolResult(BaseModel):
    result: bool
