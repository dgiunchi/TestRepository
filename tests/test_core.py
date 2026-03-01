from __future__ import annotations

from collatz.core import collatz_next, collatz_sequence


def test_collatz_next_even():
    assert collatz_next(8) == 4


def test_collatz_next_odd():
    assert collatz_next(7) == 22


def test_sequence_trivial():
    assert collatz_sequence(1) == [1]


def test_sequence_known_prefix():
    # 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
    assert collatz_sequence(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
