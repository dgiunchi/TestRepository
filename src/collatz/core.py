"""Core Collatz functions (pure / deterministic)."""

from __future__ import annotations


def collatz_next(n: int) -> int:
    """Return the next Collatz value."""
    if n < 1:
        raise ValueError("n must be >= 1")
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def collatz_sequence(start: int, max_steps: int = 10000) -> list[int]:
    """Generate Collatz sequence from start until 1 (or max_steps)."""
    if start < 1:
        raise ValueError("start must be >= 1")
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")

    seq = [start]
    n = start
    steps = 0
    while n != 1 and steps < max_steps:
        n = collatz_next(n)
        seq.append(n)
        steps += 1
    return seq
