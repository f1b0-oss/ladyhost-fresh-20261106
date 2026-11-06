"""Numeric statistics for iterables that may only be consumed once."""

import math
import statistics


def mean(values):
    """Return the arithmetic mean of finite int/float values in one pass.

    Raise ValueError for empty input or non-finite floats, and TypeError for
    other element types (including bool). The iterable need not have a length.
    """
    def validated_values():
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError("mean values must be int or float")
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("mean values must be finite")
            yield value

    try:
        return statistics.mean(validated_values())
    except statistics.StatisticsError as exc:
        raise ValueError("mean requires at least one value") from exc
