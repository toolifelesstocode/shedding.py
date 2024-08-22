import typing as t
import typing_extensions as te
import attrs
import abc

if t.TYPE_CHECKING:
    from ...api.client import Client
    from ... import types

__all__: t.Sequence[str] = (
    "BaseNestedNearbyArea",
    "NestedNearbyArea",
    "BaseNearbyArea",
    "NearbyArea",
)


class BaseNestedNearbyArea(abc.ABC):
    __slots__ = ()

    count: int
    id: str
    name: str
    region: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedNearbyAreaInformation",
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NestedNearbyArea(BaseNestedNearbyArea):
    client: "Client"

    count: int = attrs.field(repr=True)
    id: str = attrs.field(repr=True)
    name: str = attrs.field(repr=True)
    region: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedNearbyAreaInformation",
    ) -> te.Self:
        return cls(
            client=client,
            count=payload["count"],
            id=payload["id"],
            name=payload["name"],
            region=payload["region"],
        )


class BaseNearbyArea(abc.ABC):
    __slots__ = ()

    areas: t.List[BaseNestedNearbyArea]

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NearbyAreaInformation",
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NearbyArea(BaseNearbyArea):
    client: Client

    areas: t.List[NestedNearbyArea] = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NearbyAreaInformation",
    ) -> te.Self:
        return cls(
            client=client,
            areas=[
                NestedNearbyArea.from_payload(client, area) for area in payload["areas"]
            ],
        )

    async def fetch_nearby_areas(self, lat: float, lon: float):
        params = {"lat": lat, "lon": lon}
        response = await self.client.request("GET", "/areas_nearby", params=params)

        return NearbyArea.from_payload(self.client, response)
