from app.database import SessionLocal
from app.models import PlayerStatistics

with SessionLocal() as session:
    statistics = session.query(PlayerStatistics).first()

    if statistics:
        print("Player:", statistics.player.name)
        print("Position:", statistics.player.position)
        print("Team:", statistics.team.name)
        print("Competition:", statistics.competition.name)
        print("Season:", statistics.season.name)
    else:
        print("No player statistics found.")