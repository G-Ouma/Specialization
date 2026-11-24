import pytest
from app.queries import search_players, compare_players, get_player_leaderboard
from app.database import TestSessionLocal
from app.models import Player, PlayerStatistics, Season


def test_search_player_by_name():
    results = search_players(name="Rashid", session_factory=TestSessionLocal)

    assert len(results) == 1
    assert results[0][0].name == "Rashid Moyo"

def test_search_players_by_position():
    results = search_players(position="Winger", session_factory=TestSessionLocal)

    assert len(results) == 1

    for player, statistics in results:
        assert player.position == "Winger"

def test_search_players_by_minimum_goals():
    results = search_players(minimum_goals=5, session_factory=TestSessionLocal)

    assert len(results) == 2

    for player, statistics in results:
        assert statistics.goals >= 5

def test_search_players_by_minimum_assists():
    results = search_players(minimum_assists=3, session_factory=TestSessionLocal)

    assert len(results) == 3

    for player, statistics in results:
        assert statistics.assists >= 3

def test_search_players_with_combined_filters():
    results = search_players(
        position="Winger",
        minimum_goals=2,
        session_factory=TestSessionLocal
    )

    assert len(results) == 1

    for player, statistics in results:
        assert player.position == "Winger"
        assert statistics.goals >= 2

def test_compare_two_players():
    results = compare_players("Rashid", "George", session_factory=TestSessionLocal)

    assert len(results) == 2
    assert results[0][0].name == "Rashid Moyo"
    assert results[1][0].name == "George Kamau"
    assert isinstance(results[0][1], dict)
    assert results[0][1]["goals"] == 15
    assert results[1][1]["goals"] == 7

def test_compare_single_competition_and_season():
    results = compare_players(
        "Rashid",
        "George",
        mode="single",
        competition="Test League",
        season="2025-26",
        session_factory=TestSessionLocal
    )

    assert len(results) == 2
    assert results[0][1]["goals"] == 15
    assert results[1][1]["goals"] == 7

def test_single_comparison_requires_competition_and_season():
    with pytest.raises(ValueError, match="requires both competition and season"):
        compare_players("Rashid", "George", mode="single", competition="Test League", session_factory=TestSessionLocal)


def test_compare_invalid_mode():
    with pytest.raises(ValueError, match="Invalid comparison mode"):
        compare_players("Rashid", "George", mode="invalid", session_factory=TestSessionLocal)


def test_compare_combined_with_competition_and_season():
    results = compare_players("Rashid", "George", mode="combined", competition="Test League", season="2025-26", session_factory=TestSessionLocal)

    assert results[0][1]["goals"] == 15
    assert results[1][1]["goals"] == 7


def test_compare_combined_with_team_filter():
    results = compare_players("Rashid", "George", mode="combined", team="Test FC", session_factory=TestSessionLocal)

    assert results[0][1]["goals"] == 15
    assert results[1][1]["goals"] == 7

def test_compare_aggregates_multiple_season_records():
    with TestSessionLocal() as session:
        original = session.query(PlayerStatistics).join(Player).filter(Player.name=='Rashid Moyo').first()

        new_season = Season(name="2024-25")
        session.add(new_season)
        session.flush()

        values = {column.name: getattr(original, column.name) for column in PlayerStatistics.__table__.columns if column.name != "id"}
        values["season_id"] = new_season.id
        values["goals"] = 5

        session.add(PlayerStatistics(**values))
        session.commit()

    results = compare_players("Rashid", "George", mode="combined", session_factory=TestSessionLocal)

    assert results[0][1]["goals"] == 20
    assert results[1][1]["goals"] == 7

def test_compare_with_unknown_player():
    with pytest.raises(ValueError, match="No player found"):
        compare_players("Unknown Player", "Rashid", session_factory=TestSessionLocal)

def test_compare_with_ambiguous_player():
    with pytest.raises(ValueError, match="Multiple players match"):
        compare_players("Robert", "Rashid", session_factory=TestSessionLocal)

def test_goals_leaderboard():
    results = get_player_leaderboard(
        statistic="goals",
        limit=5,
        session_factory=TestSessionLocal
    )

    assert len(results) == 4
    assert results[0][0].name == "Rashid Moyo"
    assert results[0][1].goals == 15

    for index in range(len(results) - 1):
        assert results[index][1].goals >= results[index + 1][1].goals

def test_leaderboard_rejects_invalid_statistic():
    with pytest.raises(ValueError, match="Invalid statistic selected"):
        get_player_leaderboard(statistic="yellow_cards", session_factory=TestSessionLocal)

def test_leaderboard_rejects_zero_limit():
    with pytest.raises(ValueError, match="Limit must be at least 1"):
        get_player_leaderboard(statistic="goals", limit=0, session_factory=TestSessionLocal)

def test_leaderboard_default_settings():
    results = get_player_leaderboard(session_factory=TestSessionLocal)

    assert len(results) == 4
    assert results[0][0].name == "Rashid Moyo"
    assert results[0][1].goals == 15

def test_leaderboard_sorts_tied_goals_by_name():
    results = get_player_leaderboard(
        statistic="goals",
        limit=4,
        session_factory=TestSessionLocal
    )

    for index in range(len(results) - 1):
        current = results[index][1].goals
        following = results[index + 1][1].goals

        if current == following:
            assert results[index][0].name <= results[index + 1][0].name