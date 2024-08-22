import typing as t
import attrs
import typing_extensions as te
import abc

if t.TYPE_CHECKING:
    from ..api.client import Client
    from .. import types

__all__ = (
    "NestedAllowance",
    "Allowance",
)


@attrs.define(kw_only=True, slots=True)
class NestedAllowance(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    count: int = attrs.field(repr=True)
    limit: int = attrs.field(repr=True)
    type_: str = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedAllowance",
    ) -> te.Self:
        return cls(
            client=client,
            count=payload["count"],
            limit=payload["limit"],
            type_=payload["type"],
        )


@attrs.define(kw_only=True, slots=True)
class Allowance(abc.ABC):
    client: "Client" = attrs.field(repr=False)

    allowance: NestedAllowance = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.Allowance",
    ) -> te.Self:
        return cls(
            client=client,
            allowance=NestedAllowance.from_payload(
                client,
                payload=payload["allowance"],
            ),
        )

    async def fetch_allowance(self):
        response = await self.client.request("GET", "/api_allowance")

        return NestedAllowance.from_payload(self.client, response)
