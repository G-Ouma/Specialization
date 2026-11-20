from sqlalchemy import func
from app.database import SessionLocal
from app.models import Player, PlayerStatistics, Team, Competition, Season


def search_players(
    name=None,
    position=None,
    minimum_goals=None,
    minimum_assists=None,
    skip=0,
    limit=10,
    session_factory=SessionLocal
):
    with session_factory() as session:
        query = (session.query(Player, PlayerStatistics).join(PlayerStatistics))

        if name:
            query = query.filter(Player.name.ilike(f"%{name}%"))

        if position:
            query = query.filter(Player.position.ilike(position))

        if minimum_goals is not None:
            query = query.filter(PlayerStatistics.goals >= minimum_goals)

        if minimum_assists is not None:
            query = query.filter(PlayerStatistics.assists >= minimum_assists)

        return (
            query
            .order_by(PlayerStatistics.goals.desc(), Player.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )


def count_players(
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
            query = query.filter(Player.position.ilike(f"%{position}%"))

        if minimum_goals is not None:
            query = query.filter(PlayerStatistics.goals >= minimum_goals)

        if minimum_assists is not None:
            query = query.filter(PlayerStatistics.assists >= minimum_assists)

        return query.count()


def get_dashboard_stats(session_factory=SessionLocal):
    with session_factory() as session:
        total_players = session.query(Player).count()

        top_goals = (session.query(PlayerStatistics.goals).order_by(PlayerStatistics.goals.desc()).first())

        total_positions = (session.query(func.count(func.distinct(Player.position))).filter(Player.position.isnot(None)).scalar())

        return {
            "total_players": total_players,
            "top_goals": top_goals[0] if top_goals else 0,
            "total_positions": total_positions
        }


def compare_players(player_name_1, player_name_2, session_factory=SessionLocal):
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


def get_player_profile(player_name, session_factory=SessionLocal):
    with session_factory() as session:
        result = (
            session.query(Player, PlayerStatistics, Team, Competition, Season)
            .join(PlayerStatistics, Player.id == PlayerStatistics.player_id)
            .join(Team, PlayerStatistics.team_id == Team.id)
            .join(Competition, PlayerStatistics.competition_id == Competition.id)
            .join(Season, PlayerStatistics.season_id == Season.id)
            .filter(Player.name.ilike(player_name))
            .first()
        )

        if not result:
            return None

        player, stats, team, competition, season = result

        positional_players = (
            session.query(Player, PlayerStatistics)
            .join(PlayerStatistics, Player.id == PlayerStatistics.player_id)
            .filter(
                Player.position == player.position,
                PlayerStatistics.competition_id == competition.id,
                PlayerStatistics.season_id == season.id
            )
            .all()
        )

        positional_count = len(positional_players)

        goals_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.goals or 0) > (stats.goals or 0)
        )

        assists_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.assists or 0) > (stats.assists or 0)
        )

        passing_accuracy_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.pass_accuracy or 0) > (stats.pass_accuracy or 0)
        )

        tackles_won_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.tackles_won or 0) > (stats.tackles_won or 0)
        )

        interceptions_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.interceptions or 0) > (stats.interceptions or 0)
        )

        chances_created_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.chances_created or 0) > (stats.chances_created or 0)
        )

        dribbles_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.dribbles or 0) > (stats.dribbles or 0)
        )

        aerial_duels_won_rank = 1 + sum(
            1
            for _, other_stats in positional_players
            if (other_stats.aerial_duels_won or 0) > (stats.aerial_duels_won or 0)
        )

        statistics = {
            column.name: getattr(stats, column.name)
            for column in PlayerStatistics.__table__.columns
            if column.name not in {
                "id",
                "player_id",
                "team_id",
                "competition_id",
                "season_id"
            }
        }

        return {
            "name": player.name,
            "position": player.position,
            "team": team.name,
            "competition": competition.name,
            "season": season.name,
            "positional_ranking": {
                "players_in_position": positional_count,
                "goals_rank": goals_rank,
                "assists_rank": assists_rank,
                "passing_accuracy_rank": passing_accuracy_rank,
                "tackles_won_rank": tackles_won_rank,
                "interceptions_rank": interceptions_rank,
                "chances_created_rank": chances_created_rank,
                "dribbles_rank": dribbles_rank,
                "aerial_duels_won_rank": aerial_duels_won_rank
            },
            "statistics": statistics
        }
