"""Experiment helpers.

Keep reusable experiment logic here and expose small CLI scripts under `scripts/`.
"""

from __future__ import annotations

import numpy as np


def parity_proxy(z: np.ndarray) -> np.ndarray:
    """Return an analytic proxy for parity.

    For integer inputs n, this equals:
    - 0 for even n
    - 1 for odd n
    """
    return 0.5 * (1.0 - np.cos(np.pi * z))


def complex_collatz_step(z: np.ndarray) -> np.ndarray:
    """Complex extension that matches Collatz on integer points."""
    p = parity_proxy(z)
    return (1.0 - p) * (z / 2.0) + p * (3.0 * z + 1.0)


def complex_escape_grid(
    re_min: float,
    re_max: float,
    im_min: float,
    im_max: float,
    width: int,
    height: int,
    max_steps: int,
    escape_radius: float,
) -> dict[str, np.ndarray]:
    """Compute escape-time style metrics for the complex Collatz extension."""
    xs = np.linspace(re_min, re_max, width)
    ys = np.linspace(im_min, im_max, height)
    grid = xs[None, :] + 1j * ys[:, None]

    z = grid.copy()
    escaped_at = np.full((height, width), max_steps, dtype=np.int32)
    escaped = np.zeros((height, width), dtype=bool)
    min_dist_to_one = np.abs(z - 1.0)

    for step in range(max_steps):
        active = ~escaped
        if not np.any(active):
            break

        with np.errstate(over="ignore", invalid="ignore"):
            z[active] = complex_collatz_step(z[active])

        current_dist = np.abs(z - 1.0)
        np.minimum(min_dist_to_one, current_dist, out=min_dist_to_one)

        newly_escaped = (~escaped) & (np.abs(z) > escape_radius)
        escaped_at[newly_escaped] = step + 1
        escaped |= newly_escaped

    return {
        "xs": xs,
        "ys": ys,
        "escape_steps": escaped_at,
        "escaped_mask": escaped,
        "min_dist_to_one": min_dist_to_one,
    }


def generalized_next(
    n: int,
    divisor: int = 2,
    nondiv_multiplier: int = 3,
    nondiv_increment: int = 1,
) -> int:
    """Generalized Collatz-like rule.

    If n is divisible by `divisor`, return n // divisor.
    Otherwise return nondiv_multiplier * n + nondiv_increment.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if divisor < 2:
        raise ValueError("divisor must be >= 2")
    if nondiv_multiplier < 1:
        raise ValueError("nondiv_multiplier must be >= 1")

    if n % divisor == 0:
        return n // divisor
    return nondiv_multiplier * n + nondiv_increment


def generalized_sequence(
    start: int,
    max_steps: int = 10000,
    divisor: int = 2,
    nondiv_multiplier: int = 3,
    nondiv_increment: int = 1,
    stop_at: int = 1,
) -> list[int]:
    """Generate trajectory under generalized rule until stop_at or max_steps."""
    if start < 1:
        raise ValueError("start must be >= 1")
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")
    if stop_at < 1:
        raise ValueError("stop_at must be >= 1")

    seq = [start]
    n = start
    steps = 0
    while n != stop_at and steps < max_steps:
        n = generalized_next(
            n,
            divisor=divisor,
            nondiv_multiplier=nondiv_multiplier,
            nondiv_increment=nondiv_increment,
        )
        seq.append(n)
        steps += 1
    return seq


def residue_transition_matrix(
    limit: int,
    modulus: int,
    max_steps: int = 10000,
    divisor: int = 2,
    nondiv_multiplier: int = 3,
    nondiv_increment: int = 1,
    stop_at: int = 1,
) -> dict[str, object]:
    """Build a residue-class transition matrix from trajectories 1..limit."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    if modulus < 2:
        raise ValueError("modulus must be >= 2")

    matrix = np.zeros((modulus, modulus), dtype=np.int64)
    terminated = 0
    unresolved = 0
    total_edges = 0

    for start in range(1, limit + 1):
        seq = generalized_sequence(
            start=start,
            max_steps=max_steps,
            divisor=divisor,
            nondiv_multiplier=nondiv_multiplier,
            nondiv_increment=nondiv_increment,
            stop_at=stop_at,
        )
        if seq[-1] == stop_at:
            terminated += 1
        else:
            unresolved += 1

        for a, b in zip(seq, seq[1:]):
            matrix[a % modulus, b % modulus] += 1
            total_edges += 1

    return {
        "matrix": matrix,
        "terminated": terminated,
        "unresolved": unresolved,
        "total_edges": total_edges,
        "limit": limit,
        "modulus": modulus,
    }
