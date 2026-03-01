"""Statistics and summaries for Collatz trajectories."""

from __future__ import annotations

from collections import Counter

from .core import collatz_sequence


def stopping_time(start: int, max_steps: int = 10000) -> int | None:
    """Return number of steps required to reach 1, else None if capped."""
    seq = collatz_sequence(start, max_steps=max_steps)
    if seq[-1] != 1:
        return None
    return len(seq) - 1


def analyze_range(limit: int, max_steps: int = 10000) -> dict[str, object]:
    """Analyze starts 1..limit and return summary statistics."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    max_time_start = 1
    max_time = 0
    max_peak_start = 1
    max_peak = 1
    unresolved = 0
    time_buckets: Counter[int] = Counter()

    for start in range(1, limit + 1):
        seq = collatz_sequence(start, max_steps=max_steps)
        if seq[-1] != 1:
            unresolved += 1
            continue

        time = len(seq) - 1
        peak = max(seq)

        if time > max_time:
            max_time = time
            max_time_start = start

        if peak > max_peak:
            max_peak = peak
            max_peak_start = start

        bucket = (time // 10) * 10
        time_buckets[bucket] += 1

    return {
        "limit": limit,
        "max_time_start": max_time_start,
        "max_time": max_time,
        "max_peak_start": max_peak_start,
        "max_peak": max_peak,
        "unresolved": unresolved,
        "time_buckets": dict(sorted(time_buckets.items())),
    }
