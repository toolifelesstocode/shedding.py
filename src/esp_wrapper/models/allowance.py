import typing as t
import attrs
import typing_extensions as te
import abc

from esp_wrapper.api.client import Client

from .. import types

if t.TYPE_CHECKING:
    from ..api.client import Client


class BaseNestedAllowance(abc.ABC):
    __slots__ = ()

    count: int
    limit: int
    type_: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.NestedAllowance
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NestedAllowance(BaseNestedAllowance):
    client: Client

    count: int = attrs.field(repr=True)
    limit: int = attrs.field(repr=True)
    type_: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.NestedAllowance
    ) -> te.Self:
        return cls(
            client=client,
            count=payload["count"],
            limit=payload["limit"],
            type_=payload["type"],
        )


class BaseAllowance(abc.ABC):
    __slots__ = ()

    allowance: BaseNestedAllowance

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.Allowance
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class Allowance(BaseAllowance):
    client: Client

    allowance: NestedAllowance = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.Allowance
    ) -> te.Self:
        return cls(
            client=client,
            allowance=NestedAllowance.from_payload(client, payload=payload["allowance"]),
        )

    async def fetch_allowance(self):
        response = await self.client.request("GET", "/api_allowance")

        return NestedAllowance.from_payload(self.client, response)
