import abc
import datetime
import typing as t
import attrs
import typing_extensions as te

if t.TYPE_CHECKING:
    from ..api.client import Client
    from .. import types

__all__: t.Sequence[str] = (
    "NestedNearbyTopic",
    "NearbyTopic",
)


@attrs.define(kw_only=True, slots=True)
class NestedNearbyTopic(abc.ABC):
    client: "Client"

    active: datetime.datetime = attrs.field(repr=True)
    body: str = attrs.field(repr=False)
    category: str = attrs.field(repr=True)
    distance: float = attrs.field(repr=True)
    followers: int = attrs.field(repr=True)
    timestamp: datetime.datetime = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: "types.NestedNearbyTopicInformation",
    ) -> te.Self:
        return cls(
            client=client,
            active=datetime.datetime.fromisoformat(payload["active"]),
            body=payload["body"],
            category=payload["category"],
            distance=payload["distance"],
            followers=payload["followers"],
            timestamp=datetime.datetime.fromisoformat(payload["timestamp"]),
        )


@attrs.define(kw_only=True, slots=True)
class NearbyTopic(abc.ABC):
    client: "Client"

    topics: t.List[NestedNearbyTopic] = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NearbyTopicInformation",
    ) -> te.Self:
        return cls(
            client=client,
            topics=[
                NestedNearbyTopic.from_payload(client, topic)
                for topic in payload["topics"]
            ],
        )

    async def fetch_nearby_topics(self, lat: float, lon: float):
        params = {"lat": lat, "lon": lon}
        response = await self.client.request("GET", "/topics_nearby", params=params)

        return NestedNearbyTopic.from_payload(self.client, response)
