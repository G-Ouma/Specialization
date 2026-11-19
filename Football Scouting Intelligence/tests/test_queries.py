import pytest
from app.queries import (
    search_players,
    compare_players,
    get_player_leaderboard
)


def test_search_player_by_name():
    results = search_players(name="Rashid")

    assert len(results) == 1
    assert results[0][0].name == "Rashid Moyo"

def test_search_players_by_position():
    results = search_players(position="Winger")

    assert len(results) == 5

    for player, statistics in results:
        assert player.position == "Winger"

def test_search_players_by_minimum_goals():
    results = search_players(minimum_goals=5)

    assert len(results) == 4

    for player, statistics in results:
        assert statistics.goals >= 5

def test_search_players_by_minimum_assists():
    results = search_players(minimum_assists=3)

    assert len(results) == 4

    for player, statistics in results:
        assert statistics.assists >= 3

def test_search_players_with_combined_filters():
    results = search_players(
        position="Winger",
        minimum_goals=2
    )

    assert len(results) == 3

    for player, statistics in results:
        assert player.position == "Winger"
        assert statistics.goals >= 2

def test_compare_two_players():
    results = compare_players("Rashid", "George")

    assert len(results) == 2
    assert results[0][0].name == "Rashid Moyo"
    assert results[1][0].name == "George Kamau"

def test_compare_with_unknown_player():
    with pytest.raises(ValueError, match="No player found"):
        compare_players("Unknown Player", "Rashid")

def test_compare_with_ambiguous_player():
    with pytest.raises(ValueError, match="Multiple players match"):
        compare_players("Robert", "Rashid")

def test_goals_leaderboard():
    results = get_player_leaderboard(
        statistic="goals",
        limit=5
    )

    assert len(results) == 5
    assert results[0][0].name == "Rashid Moyo"
    assert results[0][1].goals == 15

    for index in range(len(results) - 1):
        assert results[index][1].goals >= results[index + 1][1].goals

def test_leaderboard_rejects_invalid_statistic():
    with pytest.raises(ValueError, match="Invalid statistic selected"):
        get_player_leaderboard(statistic="yellow_cards")

def test_leaderboard_rejects_zero_limit():
    with pytest.raises(ValueError, match="Limit must be at least 1"):
        get_player_leaderboard(statistic="goals", limit=0)

def test_leaderboard_default_settings():
    results = get_player_leaderboard()

    assert len(results) == 10
    assert results[0][0].name == "Rashid Moyo"
    assert results[0][1].goals == 15

def test_leaderboard_sorts_tied_goals_by_name():
    results = get_player_leaderboard(
        statistic="goals",
        limit=10
    )

    for index in range(len(results) - 1):
        current = results[index][1].goals
        following = results[index + 1][1].goals

        if current == following:
            assert results[index][0].name <= results[index + 1][0].name