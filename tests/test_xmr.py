import pytest

from spc.xmr import xmr_limits


def test_limits_from_known_series():
    limits = xmr_limits([10, 12, 11, 13, 12])
    assert limits.mean == pytest.approx(11.6)
    assert limits.mean_moving_range == pytest.approx(1.5)
    assert limits.upper == pytest.approx(11.6 + 2.66 * 1.5)
