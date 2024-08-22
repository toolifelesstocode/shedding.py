import typing as t
import typing_extensions as te
import attrs
import abc

from esp_wrapper.api.client import Client

from .info import BaseNestedArea

from ... import types

if t.TYPE_CHECKING:
    from ...api.client import Client

__all__: t.Sequence[str] = (
    "BaseNestedAreaSearch",
    "NestedAreaSearch",
    "BaseAreaSearch",
    "AreaSearch",
)


class BaseNestedAreaSearch(BaseNestedArea):
    __slots__ = ()

    id_: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.NestedAreaSearchInformation,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NestedAreaSearch(BaseNestedArea):
    client: Client

    id_: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.NestedAreaSearchInformation,
    ) -> te.Self:
        return cls(client=client, id_=payload["id"])


class BaseAreaSearch(abc.ABC):
    __slots__ = ()

    areas: BaseNestedAreaSearch

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self],
        client: Client,
        payload: types.AreaSearchInformation,
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class AreaSearch(BaseAreaSearch):
    client: Client

    areas: t.List[NestedAreaSearch]

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.AreaSearchInformation
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

        return BaseAreaSearch.from_payload(self.client, response)
