
import pytest

from app.database import TestSessionLocal, create_test_tables
from app.models import (
    Player,
    PlayerStatistics,
    Team,
    Competition,
    Season
)


@pytest.fixture(autouse=True)
def setup_test_database():
    create_test_tables()

    with TestSessionLocal() as session:
        # Clear existing test data
        session.query(PlayerStatistics).delete()
        session.query(Player).delete()
        session.query(Team).delete()
        session.query(Competition).delete()
        session.query(Season).delete()

        # Create shared records
        team = Team(name="Test FC")
        competition = Competition(name="Test League")
        season = Season(name="2025-26")

        session.add_all([team, competition, season])
        session.flush()

        # Create sample players
        players_data = [
            ("Rashid Moyo", "Striker", 15, 4),
            ("George Kamau", "Attacking Midfielder", 7, 5),
            ("Robert Mutua", "Midfielder", 3, 3),
            ("Robert Otieno", "Winger", 2, 1),
        ]

        for name, position, goals, assists in players_data:
            player = Player(name=name, position=position)
            session.add(player)
            session.flush()

            statistics = PlayerStatistics(
                player_id=player.id,
                team_id=team.id,
                competition_id=competition.id,
                season_id=season.id,
                goals=goals,
                assists=assists,
                pass_accuracy=80.0,
                interceptions=5,
                tackles_won=3
            )

            session.add(statistics)

        session.commit()
