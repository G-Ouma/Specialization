from fastapi.testclient import TestClient
from app.main import app
from app.main import get_session_factory
from app.database import TestSessionLocal

app.dependency_overrides[get_session_factory] = lambda: TestSessionLocal

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Football Scouting Intelligence API is running!"
    }

def test_get_all_players():
    response = client.get("/players")

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 4
    assert players[0]["name"] == "Rashid Moyo"

def test_search_player_by_name():
    response = client.get("/players", params={"name": "Rashid"})

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 1
    assert players[0]["name"] == "Rashid Moyo"


def test_search_players_with_combined_filters():
    response = client.get(
        "/players",
        params={
            "position": "Winger",
            "minimum_goals": 2
        }
    )

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 1

    for player in players:
        assert player["position"] == "Winger"
        assert player["goals"] >= 2

def test_compare_two_players():
    response = client.get(
        "/players/compare",
        params={
            "player1": "Rashid",
            "player2": "George"
        }
    )

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 2
    assert players[0]["name"] == "Rashid Moyo"
    assert players[1]["name"] == "George Kamau"


def test_compare_with_unknown_player():
    response = client.get(
        "/players/compare",
        params={
            "player1": "Unknown Player",
            "player2": "Rashid"
        }
    )

    assert response.status_code == 404


def test_compare_with_ambiguous_player():
    response = client.get(
        "/players/compare",
        params={
            "player1": "Robert",
            "player2": "Rashid"
        }
    )

    assert response.status_code == 400


def test_compare_player_with_themselves():
    response = client.get(
        "/players/compare",
        params={
            "player1": "Rashid",
            "player2": "Rashid Moyo"
        }
    )

    assert response.status_code == 400

def test_player_leaderboard_default():
    response = client.get("/players/leaderboard")

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 4
    assert players[0]["name"] == "Rashid Moyo"
    assert players[0]["value"] == 15


def test_player_leaderboard_with_assists():
    response = client.get(
        "/players/leaderboard",
        params={
            "statistic": "assists",
            "limit": 4
        }
    )

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 4
    assert players[0]["statistic"] == "assists"


def test_leaderboard_rejects_invalid_statistic():
    response = client.get("/players/leaderboard", params={"statistic": "yellow_cards"})

    assert response.status_code == 400


def test_leaderboard_rejects_zero_limit():
    response = client.get("/players/leaderboard", params={"limit": 0})

    assert response.status_code == 422