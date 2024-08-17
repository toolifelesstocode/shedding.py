import typing as t

__all__: t.Sequence[str] = (
    "AreaEvent",
    "NestedAreaInformation",
    "NestedAreaSearchInformation",
    "AreaScheduleDay",
    "AreaSchedule",
    "AreaSearchInformation",
    "AreaInformation",
    "NestedNearbyAreaInformation",
    "NearbyAreaInformation",
)


class AreaEvent(t.TypedDict):
    end: str
    note: str
    start: str


class NestedAreaInformation(t.TypedDict):
    name: str
    region: str


class NestedAreaSearchInformation(NestedAreaInformation):
    id: str


class AreaScheduleDay(t.TypedDict):
    day: str
    name: str
    stages: t.List[t.List[str]]


class AreaSchedule(t.TypedDict):
    days: t.List[AreaScheduleDay]
    source: str


class AreaSearchInformation(t.TypedDict):
    areas: t.List[NestedAreaSearchInformation]


class AreaInformation(t.TypedDict):
    events: t.List[AreaEvent]
    info: NestedAreaInformation
    schedule: AreaSchedule


class NestedNearbyAreaInformation(t.TypedDict):
    count: int
    id: str
    name: str
    region: str


class NearbyAreaInformation(t.TypedDict):
    areas: t.List[NestedNearbyAreaInformation]
