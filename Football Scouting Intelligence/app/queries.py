from app.database import SessionLocal
from app.models import Player, PlayerStatistics


def search_players(
    position=None,
    minimum_goals=None,
    minimum_assists=None
):
    with SessionLocal() as session:
        query = (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
        )

        if position:
            query = query.filter(Player.position == position)

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


def compare_players(player_name_1, player_name_2):
    with SessionLocal() as session:
        return (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics)
            .filter(
                Player.name.in_([player_name_1, player_name_2])
            )
            .all()
        )


def get_player_leaderboard(statistic="goals", limit=10):
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

    with SessionLocal() as session:
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
