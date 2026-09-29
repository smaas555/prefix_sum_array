# Prefix Sum Array

Precomputes cumulative sums so that any fixed-range sum query over an immutable sequence answers in O(1) time.

```python
from prefix_sum_array import PrefixSumArray

psa = PrefixSumArray([3, 1, 4, 1, 5, 9, 2, 6])
psa.range_sum(2, 6)   # 4 + 1 + 5 + 9 == 19.0
psa.total()           # 31.0
len(psa)              # 8
```

## Why this exists

Answering "sum of elements from i to j" repeatedly over the same array is wasteful: each query is O(n) if you re-scan. This library builds a prefix array once, in O(n), after which every query is two array lookups and a subtraction. The trade-off is immutability — the data is frozen at construction. If you need point updates between queries, use a Fenwick tree instead; this library is for the common case where the array is fixed and queries are many.

## Edge cases

`range_sum(i, j)` follows Python slice semantics: `i` is inclusive, `j` is exclusive, negatives count from the end, and out-of-range indices clamp to the bounds rather than raising. An empty range (`i == j`) returns `0.0`. A range where the clamped start exceeds the clamped end also returns `0.0` rather than erroring. Non-integer indices (including `bool`) raise `TypeError` — clamping `1.5` to `1` would hide caller mistakes.

Values are accumulated as Python floats, so integer inputs lose their `int` type in results. This keeps behaviour uniform across numeric inputs and avoids a parallel integer code path that would double the surface area for the same constant-time guarantee.
