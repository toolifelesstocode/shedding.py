import typing as t

__all__: t.Sequence[str] = (
    "NestedAllowance",
    "Allowance",
)


class NestedAllowance(t.TypedDict):
    count: int
    limit: int
    type: str


class Allowance(t.TypedDict):
    allowance: NestedAllowance
