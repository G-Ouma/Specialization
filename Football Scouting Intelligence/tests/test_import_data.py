import pytest

from app.import_data import validate_player_statistics, convert_value


def test_valid_statistics():
    stats = {"goals": 5, "pass_accuracy": 85.5}
    assert validate_player_statistics(stats, "Test Player") == []


@pytest.mark.parametrize("percentage", [-1, 101, 120])
def test_invalid_percentages(percentage):
    stats = {"pass_accuracy": percentage}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_negative_goals():
    stats = {"goals": -2}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_negative_per_90_statistics():
    stats = {"goals_per_90": -0.5}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_crosses_completed_exceed_attempts():
    stats = {"crosses_attempted": 5, "crosses_complete": 8}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_aerial_duels_won_exceed_total():
    stats = {"aerial_duels_won": 8, "aerial_duels_total": 5}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_starts_exceed_matches():
    stats = {"estimated_starts": 15, "matches": 10}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_sub_appearances_exceed_matches():
    stats = {"estimated_sub_apps": 12, "matches": 10}
    errors = validate_player_statistics(stats, "Test Player")
    assert len(errors) == 1


def test_valid_integer_conversion():
    assert convert_value("goals", 4.0) == 4


def test_decimal_rejected_for_integer_field():
    with pytest.raises(ValueError):
        convert_value("goals", 4.8)


def test_float_conversion():
    assert convert_value("pass_accuracy", 85.5) == 85.5


def test_missing_value_conversion():
    assert convert_value("goals", None) is None
