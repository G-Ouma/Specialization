from app.database import SessionLocal
from app.models import Player, PlayerStatistics


def search_players(
    name=None,
    position=None,
    minimum_goals=None,
    minimum_assists=None,
    session_factory=SessionLocal
):
    with session_factory() as session:
        query = (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
        )

        if name:
            query = query.filter(Player.name.ilike(f"%{name}%"))

        if position:
            query = query.filter(Player.position.ilike(position))

        if minimum_goals is not None:
            query = query.filter(
                PlayerStatistics.goals >= minimum_goals
            )

        if minimum_assists is not None:
            query = query.filter(
                PlayerStatistics.assists >= minimum_assists
            )

        return query.order_by(
            PlayerStatistics.goals.desc(),
            Player.name.asc()
        ).all()



def compare_players(
        player_name_1, 
        player_name_2,
        session_factory=SessionLocal
        ):
    with session_factory() as session:

        # Find the first player
        player_1 = (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
            .filter(Player.name.ilike(f"%{player_name_1}%"))
            .all()
        )

        # Find the second player
        player_2 = (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
            .filter(Player.name.ilike(f"%{player_name_2}%"))
            .all()
        )

        # Validate the first player
        if len(player_1) == 0:
            raise ValueError(f"No player found matching '{player_name_1}'")

        if len(player_1) > 1:
            raise ValueError(f"Multiple players match '{player_name_1}'. Please provide a more specific name.")

        # Validate the second player
        if len(player_2) == 0:
            raise ValueError(f"No player found matching '{player_name_2}'")

        if len(player_2) > 1:
            raise ValueError(f"Multiple players match '{player_name_2}'. Please provide a more specific name.")

        # Prevent comparing a player against themselves
        if player_1[0][0].id == player_2[0][0].id:
            raise ValueError("Please select two different players.")

        return [player_1[0], player_2[0]]



def get_player_leaderboard(statistic="goals", limit=10, session_factory=SessionLocal):
    allowed_statistics = {
        "goals",
        "assists",
        "goals_per_90",
        "assists_per_90",
        "pass_accuracy",
        "interceptions",
        "tackles_won",
    }

    if statistic not in allowed_statistics:
        raise ValueError("Invalid statistic selected.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    with session_factory() as session:
        return (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
            .filter(
                getattr(PlayerStatistics, statistic).isnot(None)
            )
            .order_by(
                getattr(PlayerStatistics, statistic).desc(),
                Player.name.asc()
            )
            .limit(limit)
            .all()
        )
