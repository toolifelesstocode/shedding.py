import abc
import datetime
import typing as t
import attrs
import typing_extensions as te

if t.TYPE_CHECKING:
    from ..api.client import Client
    from .. import types

__all__: t.Sequence[str] = (
    "Stage",
    "StatusRegion",
    "NestedStatus",
    "Status",
)


@attrs.define(kw_only=True, slots=True)
class Stage(abc.ABC):
    client: "Client"

    stage: int = attrs.field(repr=True)
    stage_start_timestamp: datetime.datetime = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.StageInformation",
    ) -> te.Self:
        return cls(
            client=client,
            stage=int(payload["stage"]),
            stage_start_timestamp=datetime.datetime.fromisoformat(
                payload["stage_start_timestamp"]
            ),
        )


@attrs.define(kw_only=True, slots=True)
class StatusRegion(abc.ABC):
    client: "Client"

    name: str = attrs.field(repr=True)
    next_stages: t.List[Stage] = attrs.field(repr=False)
    stage: str = attrs.field(repr=True)
    stage_updated: datetime.datetime = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.StatusRegionInformation",
    ):
        return cls(
            client=client,
            name=payload["name"],
            next_stages=[
                Stage.from_payload(client, stage) for stage in payload["next_stages"]
            ],
            stage=payload["stage"],
            stage_updated=datetime.datetime.fromisoformat(payload["stage_updated"]),
        )


@attrs.define(kw_only=True, slots=True)
class NestedStatus(abc.ABC):
    client: "Client"

    cape_town: StatusRegion = attrs.field(repr=False)
    eskom: StatusRegion = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.NestedStatusInformation",
    ) -> te.Self:
        return cls(
            client=client,
            cape_town=StatusRegion.from_payload(client, payload["capetown"]),
            eskom=StatusRegion.from_payload(client, payload["eskom"]),
        )


@attrs.define(kw_only=True, slots=True)
class Status(abc.ABC):
    client: "Client"

    status: NestedStatus = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self],
        client: "Client",
        payload: "types.StatusInformation",
    ) -> te.Self:
        return cls(
            client=client,
            status=NestedStatus.from_payload(client, payload["status"]),
        )

    async def fetch_status(
        self,
    ):
        response = await self.client.request("GET", "/status")

        return NestedStatus.from_payload(self.client, response)
