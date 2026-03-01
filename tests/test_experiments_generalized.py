from __future__ import annotations

from collatz.core import collatz_next
from collatz.experiments import generalized_next, residue_transition_matrix


def test_generalized_next_matches_classic_collatz():
    for n in range(1, 80):
        assert generalized_next(n, divisor=2, nondiv_multiplier=3, nondiv_increment=1) == collatz_next(n)


def test_residue_transition_matrix_shape_and_edges():
    result = residue_transition_matrix(limit=20, modulus=8, max_steps=50)
    matrix = result["matrix"]
    assert matrix.shape == (8, 8)
    assert int(result["total_edges"]) > 0
