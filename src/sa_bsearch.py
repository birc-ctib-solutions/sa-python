from typing import (
    Iterator, NamedTuple, Optional
)
from dataclasses import (
    dataclass
)


@dataclass
class SARange:
    sa: list[int]
    start: int
    stop: int

    def __iter__(self) -> Iterator[int]:
        for i in range(self.start, self.stop):
            yield self.sa[i]


class SearchSpace(NamedTuple):
    x: str
    sa: list[int]


class SearchRange(NamedTuple):
    offset: int
    lo: int
    hi: int


def lower(a: str, srange: SearchRange, space: SearchSpace) -> int:
    """Finds the lower bound of `a` in the block defined by `srange`."""
    offset, lo, hi = srange
    x, sa = space
    while lo < hi:
        m = (lo + hi) // 2
        if x[sa[m] + offset] < a:
            lo = m + 1
        else:
            hi = m
    return lo


def upper(a: str, srange: SearchRange, space: SearchSpace) -> int:
    """Finds the upper bound of `a` in the block defined by `srange`."""
    return lower(chr(ord(a) + 1), srange, space)


def block(a: str, srange: SearchRange, space: SearchSpace) -> SearchRange:
    """Updates srange by finding the sub-block with `a` at `offset`. The
    result is a search range with an updated `offset` and `[lo,hi)` interval.
    Returns None if the block is empty."""
    return SearchRange(
        srange.offset + 1, lower(a, srange, space), upper(a, srange, space)
    )


def sa_bsearch(p: str, x: str, sa: list[int]) -> SARange:
    space = SearchSpace(x, sa)
    srange = SearchRange(offset=0, lo=1, hi=len(sa))  # lo=1 to avoid $
    for a in p:
        srange = block(a, srange, space)
        if srange.lo == srange.hi:
            break
    return SARange(sa, srange.lo, srange.hi)
