import typing as t

__all__: t.Sequence[str] = (
    "StageInformation",
    "StatusRegionInformation",
    "NestedStatusInformation",
    "StatusInformation",
)


class StageInformation(t.TypedDict):
    stage: str
    stage_start_timestamp: str


class StatusRegionInformation(t.TypedDict):
    name: str
    next_stages: t.List[StageInformation]
    stage: str
    stage_updated: str


class NestedStatusInformation(t.TypedDict):
    capetown: StatusRegionInformation
    eskom: StatusRegionInformation


class StatusInformation(t.TypedDict):
    status: NestedStatusInformation
