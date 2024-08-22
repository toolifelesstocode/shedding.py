import datetime
import typing as t
import typing_extensions as te
import abc
import attrs

from esp_wrapper.api.client import Client

from .. import types

if t.TYPE_CHECKING:
    from ..api.client import Client


class BaseAreaEvent(abc.ABC):
    __slots__ = ()

    end: str
    note: str
    start: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaEvent,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class AreaEvent(BaseAreaEvent):
    client: Client

    end: datetime.datetime = attrs.field(repr=True)
    note: str = attrs.field(repr=True)
    start: datetime.datetime = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaEvent,
    ) -> te.Self:
        return cls(
            client=client,
            end=datetime.datetime.fromisoformat(payload["end"]),
            note=payload["note"],
            start=datetime.datetime.fromisoformat(payload["start"]),
        )


class BaseNestedArea(abc.ABC):
    __slots__ = ()

    name: str
    region: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.NestedAreaInformation,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NestedArea(BaseNestedArea):
    client: Client

    name: str = attrs.field(repr=True)
    region: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.NestedAreaInformation,
    ) -> te.Self:
        return cls(
            client=client,
            name=payload["name"],
            region=payload["region"],
        )


class BaseAreaScheduleDay(abc.ABC):
    __slots__ = ()

    date: str
    name: str
    stages: t.List[t.List[str]]

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaScheduleDay,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class AreaScheduleDay(BaseAreaScheduleDay):
    client: Client

    date: datetime.date = attrs.field(repr=True)
    name: str = attrs.field(repr=True)
    stages: t.List[t.List[str]] = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaScheduleDay,
    ) -> te.Self:
        return cls(
            client=client,
            date=datetime.date.fromisoformat(payload["date"]),
            name=payload["name"],
            stages=payload["stages"],
        )


class BaseAreaSchedule(abc.ABC):
    __slots__ = ()

    days: t.List[BaseAreaScheduleDay]
    source: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaSchedule,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class AreaSchedule(BaseAreaSchedule):
    client: Client

    days: t.List[AreaScheduleDay] = attrs.field(repr=True)
    source: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaSchedule,
    ) -> te.Self:
        return cls(
            client=client,
            days=[AreaScheduleDay.from_payload(client, day) for day in payload["days"]],
            source=payload["source"],
        )


class BaseArea(abc.ABC):
    __slots__ = ()

    events: t.List[BaseAreaEvent]
    info: BaseNestedArea
    schedule: BaseAreaSchedule

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaInformation,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class Area(BaseArea):
    client: Client

    events: t.List[AreaEvent] = attrs.field(repr=True)
    info: NestedArea = attrs.field(repr=True)
    schedule: AreaSchedule = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaInformation,
    ) -> te.Self:
        return cls(
            client=client,
            events=[
                AreaEvent.from_payload(client, event) for event in payload["events"]
            ],
            info=NestedArea.from_payload(client=client, payload=payload["info"]),
            schedule=AreaSchedule.from_payload(client, payload["schedule"]),
        )

    async def fetch_area_information(self, id: str):
        params = {"id": id}
        response = await self.client.request("GET", "/area", params=params)

        return Area.from_payload(self.client, response)
