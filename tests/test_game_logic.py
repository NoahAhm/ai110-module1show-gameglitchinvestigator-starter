from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess


def test_winning_guess_returns_win_outcome():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high_returns_too_high_outcome():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low_returns_too_low_outcome():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_direction_regression_for_too_high_guess():
    """Regression test: too-high guesses must tell the player to go lower."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_parse_guess_rejects_decimal_input():
    ok, value, err = parse_guess("12.5")
    assert ok is False
    assert value is None
    assert err == "That is not a whole number."


def test_get_range_for_difficulty_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)
