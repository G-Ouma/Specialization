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


def find_player(session, player_name):
    matches = session.query(Player).filter(Player.name.ilike(f"%{player_name}%")).all()

    if not matches:
        raise ValueError(f"No player found matching '{player_name}'")

    if len(matches) > 1:
        raise ValueError(f"Multiple players match '{player_name}'. Please provide a more specific name.")

    return matches[0]


def get_player_statistics(session, player_id, competition=None, season=None, team=None):
    query = (
        session.query(PlayerStatistics)
        .filter(PlayerStatistics.player_id == player_id)
    )

    if competition:
        query = query.join(Competition).filter(Competition.name.ilike(competition))

    if season:
        query = query.join(Season).filter(Season.name.ilike(season))

    if team:
        query = query.join(Team).filter(Team.name.ilike(team))

    return query.all()


def aggregate_player_statistics(records):
    excluded_fields = {"id", "player_id", "team_id", "competition_id", "season_id", "pass_accuracy", "tackle_success_rate", "cross_accuracy", "aerial_duels_success_rate", "estimated_90s"}

    statistics = {}

    for column in PlayerStatistics.__table__.columns:
        field = column.name

        if field in excluded_fields or field.endswith("_per_90"):
            continue

        values = [getattr(record, field) for record in records if getattr(record, field) is not None]
        statistics[field] = sum(values) if values else None

    # Recalculate percentage metrics using combined totals
    percentage_fields = {
        "pass_accuracy": ("passes_complete", "passes_incomplete", "sum"),
        "tackle_success_rate": ("tackles_won", "total_tackles", "direct"),
        "cross_accuracy": ("crosses_complete", "crosses_attempted", "direct"),
        "aerial_duels_success_rate": ("aerial_duels_won", "aerial_duels_total", "direct")
    }

    for field, (numerator, denominator, method) in percentage_fields.items():
        first_value = statistics.get(numerator)
        second_value = statistics.get(denominator)

        if first_value is None or second_value is None:
            statistics[field] = None
        else:
            total = first_value + second_value if method == "sum" else second_value
            statistics[field] = round(first_value / total * 100, 2) if total else None

    # Recalculate per-90 metrics using combined minutes
    per_90_fields = {
        "passes_complete_per_90": "passes_complete",
        "passes_incomplete_per_90": "passes_incomplete",
        "goals_per_90": "goals",
        "assists_per_90": "assists",
        "shots_per_90": "shots",
        "fouls_committed_per_90": "fouls_committed",
        "tackles_won_per_90": "tackles_won",
        "tackles_lost_per_90": "tackles_lost",
        "interceptions_per_90": "interceptions",
        "crosses_attempted_per_90": "crosses_attempted",
        "crosses_complete_per_90": "crosses_complete",
        "ball_won_opponent_per_90": "ball_won_opponent_half",
        "ball_won_own_per_90": "ball_won_own_half",
        "ball_lost_own_per_90": "ball_lost_own_half",
        "ball_lost_opponent_per_90": "ball_lost_opponent_half",
        "dribbles_per_90": "dribbles",
        "box_carries_per_90": "box_carries",
        "box_touches_per_90": "box_touches",
        "progressive_passes_complete_per_90": "progressive_passes_complete",
        "progressive_passes_incomplete_per_90": "progressive_passes_incomplete"
    }

    minutes = statistics.get("estimated_minutes")

    for field, total_field in per_90_fields.items():
        total = statistics.get(total_field)
        statistics[field] = round(total / minutes * 90, 2) if total is not None and minutes else None

    statistics["estimated_90s"] = round(minutes / 90, 2) if minutes else None

    return statistics


def compare_players(player_name_1, player_name_2, mode="combined", competition=None, season=None, team=None, session_factory=SessionLocal):
    if mode not in ("single", "combined"):
        raise ValueError("Invalid comparison mode. Choose 'single' or 'combined'.")

    if mode == "single" and (not competition or not season):
        raise ValueError("Single comparison mode requires both competition and season.")

    with session_factory() as session:
        player_1 = find_player(session, player_name_1)
        player_2 = find_player(session, player_name_2)

        if player_1.id == player_2.id:
            raise ValueError("Please select two different players.")

        statistics_1 = get_player_statistics(session, player_1.id, competition, season, team)
        statistics_2 = get_player_statistics(session, player_2.id, competition, season, team)

        if not statistics_1:
            raise ValueError(f"No statistics found for {player_1.name} with the selected filters.")

        if not statistics_2:
            raise ValueError(f"No statistics found for {player_2.name} with the selected filters.")

        return [
            (player_1, aggregate_player_statistics(statistics_1)),
            (player_2, aggregate_player_statistics(statistics_2))
        ]



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
