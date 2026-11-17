from pathlib import Path

import pandas as pd

from app.database import SessionLocal
from app.models import (
    Player,
    Team,
    Competition,
    Season,
    PlayerStatistics,
)

COLUMN_MAPPING = {
    "Passes Complete": "passes_complete",
    "Passes Incomplete": "passes_incomplete",
    "Pass Accuracy %": "pass_accuracy",
    "Goals": "goals",
    "Assists": "assists",
    "Shots (in+out box)": "shots",
    "Fouls Committed": "fouls_committed",
    "Yellow Cards": "yellow_cards",
    "Red Cards": "red_cards",
    "Tackles Won": "tackles_won",
    "Tackles Lost": "tackles_lost",
    "Total Tackles": "total_tackles",
    "Tackle Success Rate %": "tackle_success_rate",
    "Tackles Won /90": "tackles_won_per_90",
    "Tackles Lost /90": "tackles_lost_per_90",
    "Interceptions": "interceptions",
    "Interceptions /90": "interceptions_per_90",
    "Crosses Attempted": "crosses_attempted",
    "Crosses Complete": "crosses_complete",
    "Cross Accuracy %": "cross_accuracy",
    "Crosses Attempted /90": "crosses_attempted_per_90",
    "Crosses Complete /90": "crosses_complete_per_90",
    "Ball Won Opp": "ball_won_opponent_half",
    "Ball Won Own": "ball_won_own_half",
    "Ball Own Lost": "ball_lost_own_half",
    "Ball Opp Lost": "ball_lost_opponent_half",
    "Dribbles": "dribbles",
    "Box Carry": "box_carries",
    "Box Touch": "box_touches",
    "Progressive Passes Complete": "progressive_passes_complete",
    "Progressive Passes Incomplete": "progressive_passes_incomplete",
    "Estimated Minutes": "estimated_minutes",
    "Matches": "matches",
    "Estimated Starts": "estimated_starts",
    "Estimated Sub Apps": "estimated_sub_apps",
    "Estimated 90s": "estimated_90s",
    "Passes Complete /90": "passes_complete_per_90",
    "Passes Incomplete /90": "passes_incomplete_per_90",
    "Goals /90": "goals_per_90",
    "Assists /90": "assists_per_90",
    "Shots (in+out box) /90": "shots_per_90",
    "Fouls Committed /90": "fouls_committed_per_90",
    "Ball Won Opp /90": "ball_won_opponent_per_90",
    "Ball Won Own /90": "ball_won_own_per_90",
    "Ball Own Lost /90": "ball_lost_own_per_90",
    "Ball Opp Lost /90": "ball_lost_opponent_per_90",
    "Dribbles /90": "dribbles_per_90",
    "Box Carry /90": "box_carries_per_90",
    "Box Touch /90": "box_touches_per_90",
    "Progressive Passes Complete /90": "progressive_passes_complete_per_90",
    "Progressive Passes Incomplete /90": "progressive_passes_incomplete_per_90",
    "Clearances": "clearances",
    "Blocks": "blocks",
    "Chances Created": "chances_created",
    "Key Pass": "key_passes",
    "Aerial Duels Won": "aerial_duels_won",
    "Aerial Duels Total": "aerial_duels_total",
    "Aerial Duels %": "aerial_duels_success_rate",
}

INTEGER_FIELDS = {
    "passes_complete", "passes_incomplete",
    "goals", "assists", "shots",
    "fouls_committed", "yellow_cards", "red_cards",
    "tackles_won", "tackles_lost", "total_tackles",
    "interceptions", "clearances", "blocks",
    "crosses_attempted", "crosses_complete",
    "ball_won_opponent_half", "ball_won_own_half",
    "ball_lost_own_half", "ball_lost_opponent_half",
    "dribbles", "box_carries", "box_touches",
    "progressive_passes_complete",
    "progressive_passes_incomplete",
    "matches", "estimated_starts", "estimated_sub_apps",
    "chances_created", "key_passes",
    "aerial_duels_won", "aerial_duels_total",
}

def convert_value(field, value):
    if pd.isna(value):
        return None

    if field in INTEGER_FIELDS:
        return int(value)

    return float(value)


def import_player_statistics():
    # Locate the project directory
    project_dir = Path(__file__).resolve().parent.parent

    # Load the cleaned player dataset
    data_file = (
        project_dir / "data" / "processed" / "players_cleaned.csv"
    )

    df = pd.read_csv(data_file)

    print("\nPlayer dataset loaded successfully!")

    # Import player statistics within a database transaction
    with SessionLocal.begin() as session:

        team = session.query(Team).filter_by(
            name="Equity FC"
        ).one()

        competition = session.query(Competition).filter_by(
            name="National Super League"
        ).one()

        season = session.query(Season).filter_by(
            name="2025-26"
        ).one()

        for _, row in df.iterrows():

            player = session.query(Player).filter_by(
                name=row["Player"]
            ).one()

            # Convert the player's statistics
            stats_data = {
                database_field: convert_value(
                    database_field, row[csv_column]
                )
                for csv_column, database_field
                in COLUMN_MAPPING.items()
            }

            # Check whether statistics already exist
            statistics = session.query(
                PlayerStatistics
            ).filter_by(
                player_id=player.id,
                team_id=team.id,
                competition_id=competition.id,
                season_id=season.id
            ).first()

            if statistics:
                # Update existing statistics
                for field, value in stats_data.items():
                    setattr(statistics, field, value)

            else:
                # Create a new statistics record
                statistics = PlayerStatistics(
                    player_id=player.id,
                    team_id=team.id,
                    competition_id=competition.id,
                    season_id=season.id,
                    **stats_data
                )

                session.add(statistics)

    print("Player statistics imported successfully!")

    # Verify the total number of records
    with SessionLocal() as session:
        total_records = session.query(
            PlayerStatistics
        ).count()

    print("Total statistics records:", total_records)


if __name__ == "__main__":
    import_player_statistics()
