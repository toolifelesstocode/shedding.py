import abc
import datetime
import typing as t
import attrs
import typing_extensions as te

from .. import types

if t.TYPE_CHECKING:
    from ..api.client import Client


class BaseStage(abc.ABC):
    __slot__ = ()

    stage: int
    stage_start_timestamp: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StageInformation
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class Stage(BaseStage):
    client: Client = attrs.field(repr=False)

    stage: int = attrs.field(repr=True)
    stage_start_timestamp: datetime.datetime = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StageInformation
    ) -> te.Self:
        return cls(
            client=client,
            stage=int(payload["stage"]),
            stage_start_timestamp=datetime.datetime.fromisoformat(
                payload["stage_start_timestamp"]
            ),
        )


class BaseStatusRegion(abc.ABC):
    __slots__ = ()

    name: str
    next_stages: t.List[BaseStage]
    stage: str
    stage_updated: str

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StatusInformation
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class StatusRegion(BaseStatusRegion):
    client: Client

    name: str = attrs.field(repr=True)
    next_stages: t.List[Stage] = attrs.field(repr=False)
    stage: str = attrs.field(repr=True)
    stage_updated: datetime.datetime = attrs.field(repr=True)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StatusRegionInformation
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


class BaseNestedStatus(abc.ABC):
    __slots__ = ()

    client: Client = attrs.field()

    cape_town: BaseStatusRegion
    eskom: BaseStatusRegion

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.NestedStatusInformation
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class NestedStatus(BaseNestedStatus):
    client: Client

    cape_town: StatusRegion = attrs.field(repr=False)
    eskom: StatusRegion = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.NestedStatusInformation
    ) -> te.Self:
        return cls(
            client=client,
            cape_town=StatusRegion.from_payload(client, payload["capetown"]),
            eskom=StatusRegion.from_payload(client, payload["eskom"]),
        )


class BaseStatus(abc.ABC):
    __slots__ = ()

    client: Client

    @classmethod
    @abc.abstractmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StatusInformation
    ) -> te.Self:
        pass


@attrs.define(kw_only=True, slots=True)
class Status(BaseStatus):
    client: Client = attrs.field(repr=False)

    status: NestedStatus = attrs.field(repr=False)

    @classmethod
    def from_payload(
        cls: type[te.Self], client: Client, payload: types.StatusInformation
    ) -> te.Self:
        return cls(
            client=client,
            status=NestedStatus.from_payload(client, payload["status"])
        )

    async def fetch_status(
        self,
        area: t.Optional[t.Literal["capetown", "eskom"]] = None,
    ):
        response = await self.client.request("GET", "/status")

        return NestedStatus.from_payload(self.client, response)
