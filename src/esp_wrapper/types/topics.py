import typing as t

__all__: t.Sequence[str] = (
    "NestedNearbyTopicInformation",
    "NearbyTopicInformation",
)


class NestedNearbyTopicInformation(t.TypedDict):
    active: str
    body: str
    category: str
    distance: float
    followers: int
    timestamp: str


class NearbyTopicInformation(t.TypedDict):
    topics: t.List[NestedNearbyTopicInformation]
