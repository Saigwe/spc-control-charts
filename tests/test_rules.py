from spc.report import run
from spc.rules import outside_limits, shift, special_causes, trend, two_of_three_near_limit
from spc.summary import assurance, variation
from spc.xmr import XmRLimits

LIMITS = XmRLimits(mean=10.0, lower=7.0, upper=13.0, mean_moving_range=3 / 2.66)  # sigma = 1


def test_outside_limits_flags_both_sides():
    assert outside_limits([10, 14, 6, 11], LIMITS) == {1: "high", 2: "low"}


def test_shift_needs_seven_points_one_side():
    assert shift([11] * 6 + [9], LIMITS) == {}
    assert set(shift([9] + [11] * 7 + [9], LIMITS)) == set(range(1, 8))


def test_trend_needs_six_increasing_points():
    assert trend([1, 2, 3, 4, 5]) == {}
    assert trend([5, 1, 2, 3, 4, 5, 6]) == {i: "high" for i in range(1, 7)}


def test_two_of_three_beyond_two_sigma():
    assert two_of_three_near_limit([10, 12.5, 10, 12.4], LIMITS) == {1: "high", 3: "high"}
    assert two_of_three_near_limit([10, 12.5, 10, 10, 12.4], LIMITS) == {}


def test_special_causes_combines_rules():
    flags = special_causes([10, 14, 10, 10], LIMITS)
    assert flags == {1: {"outside_limits"}}


def test_variation_direction_respects_polarity():
    values = [10, 10, 10, 10, 10, 6]
    assert variation(values, LIMITS, higher_is_better=False) == "special cause - improving"
    assert variation(values, LIMITS, higher_is_better=True) == "special cause - concerning"
    assert variation([10, 11, 9, 10], LIMITS, higher_is_better=True) == "common cause"


def test_assurance_compares_target_with_limits():
    assert assurance(LIMITS, 6.0, higher_is_better=True) == "consistently passing"
    assert assurance(LIMITS, 14.0, higher_is_better=True) == "consistently failing"
    assert assurance(LIMITS, 11.0, higher_is_better=True) == "hit and miss"
    assert assurance(LIMITS, 14.0, higher_is_better=False) == "consistently passing"


def test_report_detects_planted_signals(tmp_path):
    rows = {r.name: r for r in run(tmp_path)}
    assert rows["Falls per 1,000 bed days"].variation == "special cause - improving"
    assert rows["Incidents awaiting review"].variation == "special cause - concerning"
    assert rows["Complaints answered within 25 days (%)"].variation == "common cause"
    assert (tmp_path / "report.md").exists()
