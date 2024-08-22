import typing as t
import typing_extensions as te
import attrs
import abc

from .info import NestedArea

if t.TYPE_CHECKING:
    from ...api.client import Client
    from ... import types

__all__: t.Sequence[str] = (
    "NestedAreaSearch",
    "AreaSearch",
)


@attrs.define(kw_only=True, slots=True)
class NestedAreaSearch(NestedArea):
    client: "Client" = attrs.field(repr=False)

    id_: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedAreaSearchInformation",
    ) -> te.Self:
        return cls(
            client=client,
            id_=payload["id"],
            name=payload["name"],
            region=payload["region"],
        )


@attrs.define(kw_only=True, slots=True)
class AreaSearch(abc.ABC):
    client: Client = attrs.field(repr=False)

    areas: t.List[NestedAreaSearch]

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.AreaSearchInformation",
    ) -> te.Self:
        return cls(
            client=client,
            areas=[
                NestedAreaSearch.from_payload(client, area) for area in payload["areas"]
            ],
        )

    async def fetch_areas(self, text: str):
        params = {"text": text}
        response = await self.client.request("GET", "/areas_search", params=params)

        return AreaSearch.from_payload(self.client, response)
