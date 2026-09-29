"""Prefix sum array for constant-time fixed-range sum queries."""

from typing import Iterable, List, Sequence


class PrefixSumArray:
    """Precompute cumulative sums so any fixed-range sum query runs in O(1).

    The array is immutable once built. This is deliberate: supporting mutation
    would either force every query to re-validate or require a Fenwick tree,
    which is a different data structure with different constant factors. If you
    need updates, this is the wrong tool.

    Indexing convention: ``range_sum(i, j)`` returns the sum of elements from
    index ``i`` inclusive through ``j`` exclusive, matching Python's slice
    semantics. ``range_sum(0, n)`` is the total. An empty range (``i == j``)
    returns 0.
    """

    __slots__ = ("_prefix",)

    def __init__(self, data: Iterable[float] | None = None) -> None:
        # prefix[i] holds the sum of data[0:i]; prefix[0] == 0. Keeping the
        # leading zero lets range_sum(i, j) be prefix[j] - prefix[i] with no
        # special-casing for i == 0.
        source: Sequence[float] = list(data) if data is not None else []
        prefix: List[float] = [0] * (len(source) + 1)
        acc = 0.0
        for k, value in enumerate(source):
            acc += value
            prefix[k + 1] = acc
        self._prefix = prefix

    def __len__(self) -> int:
        return len(self._prefix) - 1

    def total(self) -> float:
        """Return the sum of the entire underlying array."""
        return self._prefix[-1]

    def range_sum(self, start: int, end: int) -> float:
        """Return the sum of elements from ``start`` inclusive to ``end`` exclusive.

        Negative indices are supported and interpreted as offsets from the end,
        exactly as Python slices do. Indices are clamped to the valid range
        rather than raising, so a query like ``range_sum(-100, 100)`` on a
        five-element array behaves like ``range_sum(0, 5)``.

        Raises ``TypeError`` for non-integer indices — clamping a string or
        float would hide bugs silently.
        """
        n = len(self)
        i = self._clamp_index(start, n)
        j = self._clamp_index(end, n)
        if j < i:
            return 0.0
        return self._prefix[j] - self._prefix[i]

    @staticmethod
    def _clamp_index(idx: int, n: int) -> int:
        """Normalize an index the way Python slicing does: negatives count
        from the end, out-of-range values clamp to the bounds.

        We reject non-integers explicitly. Accepting floats (e.g. ``1.5``)
        would silently truncate and produce a confusing answer; accepting them
        via ``int()`` would mask caller mistakes.
        """
        if isinstance(idx, bool) or not isinstance(idx, int):
            raise TypeError(
                f"index must be int, got {type(idx).__name__}"
            )
        if idx < 0:
            idx += n
            if idx < 0:
                return 0
        elif idx > n:
            return n
        return idx
