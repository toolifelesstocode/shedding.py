import datetime
import typing as t
import typing_extensions as te
import abc
import attrs

if t.TYPE_CHECKING:
    from ...api.client import Client
    from ... import types

__all__: t.Sequence[str] = (
    "AreaEvent",
    "NestedArea",
    "AreaScheduleDay",
    "AreaSchedule",
    "Area",
)


@attrs.define(kw_only=True, slots=True)
class AreaEvent(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    end: datetime.datetime = attrs.field(repr=True)
    note: str = attrs.field(repr=True)
    start: datetime.datetime = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.AreaEvent",
    ) -> te.Self:
        return cls(
            client=client,
            end=datetime.datetime.fromisoformat(payload["end"]),
            note=payload["note"],
            start=datetime.datetime.fromisoformat(payload["start"]),
        )


@attrs.define(kw_only=True, slots=True)
class NestedArea(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    name: str = attrs.field(repr=True)
    region: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedAreaInformation",
    ) -> te.Self:
        return cls(
            client=client,
            name=payload["name"],
            region=payload["region"],
        )


@attrs.define(kw_only=True, slots=True)
class AreaScheduleDay(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    date: datetime.date = attrs.field(repr=True)
    name: str = attrs.field(repr=True)
    stages: t.List[t.List[str]] = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.AreaScheduleDay",
    ) -> te.Self:
        return cls(
            client=client,
            date=datetime.date.fromisoformat(payload["date"]),
            name=payload["name"],
            stages=payload["stages"],
        )


@attrs.define(kw_only=True, slots=True)
class AreaSchedule(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    days: t.List[AreaScheduleDay] = attrs.field(repr=True)
    source: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.AreaSchedule",
    ) -> te.Self:
        return cls(
            client=client,
            days=[AreaScheduleDay.from_payload(client, day) for day in payload["days"]],
            source=payload["source"],
        )


@attrs.define(kw_only=True, slots=True)
class Area(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    events: t.List[AreaEvent] = attrs.field(repr=True)
    info: "NestedArea" = attrs.field(repr=True)
    schedule: "AreaSchedule" = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.AreaInformation",
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

        return self.from_payload(self.client, response)
