from __future__ import annotations

import numpy as np

from collatz.core import collatz_next
from collatz.experiments import complex_collatz_step


def test_complex_step_matches_integer_collatz():
    ints = np.arange(1, 50, dtype=float)
    z = ints.astype(np.complex128)
    stepped = complex_collatz_step(z)
    expected = np.array([collatz_next(int(n)) for n in ints], dtype=np.complex128)
    assert np.allclose(stepped, expected)
