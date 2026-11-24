from pathlib import Path

import pandas as pd

from app.database import SessionLocal
from app.models import Player, Team, Competition, Season, PlayerStatistics

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

PERCENTAGE_FIELDS = {
    "pass_accuracy",
    "tackle_success_rate",
    "cross_accuracy",
    "aerial_duels_success_rate",
}

NON_NEGATIVE_FIELDS = INTEGER_FIELDS | {
    "pass_accuracy", "tackle_success_rate", "cross_accuracy",
    "aerial_duels_success_rate",
    "tackles_won_per_90", "tackles_lost_per_90",
    "interceptions_per_90", "crosses_attempted_per_90",
    "crosses_complete_per_90", "passes_complete_per_90",
    "passes_incomplete_per_90", "goals_per_90", "assists_per_90",
    "shots_per_90", "fouls_committed_per_90",
    "ball_won_opponent_per_90", "ball_won_own_per_90",
    "ball_lost_own_per_90", "ball_lost_opponent_per_90",
    "dribbles_per_90", "box_carries_per_90", "box_touches_per_90",
    "progressive_passes_complete_per_90",
    "progressive_passes_incomplete_per_90",
    "estimated_minutes", "estimated_90s",
}



def validate_player_statistics(stats_data, player_name):
    errors = []

    for field in NON_NEGATIVE_FIELDS - PERCENTAGE_FIELDS:
        value = stats_data.get(field)

        if value is not None and value < 0:
            errors.append(f"{field} cannot be negative: {value}")

    for field in PERCENTAGE_FIELDS:
        value = stats_data.get(field)

        if value is not None and not 0 <= value <= 100:
            errors.append(f"{field} must be between 0 and 100: {value}")

    if stats_data.get("crosses_complete") is not None and stats_data.get("crosses_attempted") is not None and stats_data["crosses_complete"] > stats_data["crosses_attempted"]:
        errors.append("Crosses complete cannot exceed crosses attempted")

    if stats_data.get("aerial_duels_won") is not None and stats_data.get("aerial_duels_total") is not None and stats_data["aerial_duels_won"] > stats_data["aerial_duels_total"]:
        errors.append("Aerial duels won cannot exceed total aerial duels")

    if stats_data.get("estimated_starts") is not None and stats_data.get("matches") is not None and stats_data["estimated_starts"] > stats_data["matches"]:
        errors.append("Estimated starts cannot exceed matches")

    if stats_data.get("estimated_sub_apps") is not None and stats_data.get("matches") is not None and stats_data["estimated_sub_apps"] > stats_data["matches"]:
        errors.append("Estimated substitute appearances cannot exceed matches")

    if errors:
        print(f"\nValidation errors for {player_name}:")
        for error in errors:
            print(f" - {error}")

    return errors



def convert_value(field, value):
    if pd.isna(value):
        return None

    if field in INTEGER_FIELDS:
        numeric_value = float(value)

        if not numeric_value.is_integer():
            raise ValueError(f"{field} must be a whole number: {value}")

        return int(numeric_value)

    return float(value)


def import_player_statistics():
    # Locate the project directory
    project_dir = Path(__file__).resolve().parent.parent

    # Load the cleaned player dataset
    data_file = (project_dir / "data" / "processed" / "nsl_2025_26_players_cleaned.csv")

    df = pd.read_csv(data_file)

    valid_records = 0
    invalid_records = 0

    print("\nPlayer dataset loaded successfully!")

    # Import player statistics within a database transaction
    with SessionLocal.begin() as session:

        competition = session.query(Competition).filter_by(name="National Super League").one()

        season = session.query(Season).filter_by(name="2025-26").one()

        for _, row in df.iterrows():

            team_name = row["Team"]
            team = session.query(Team).filter_by(name=team_name).first()

            if team is None:
                team = Team(name=team_name)
                session.add(team)
                session.flush()

            player = session.query(Player).filter_by(name=row["Player"]).first()

            if player is None:
                player = Player(name=row["Player"], position=row["Position"])
                session.add(player)
                session.flush()
            else:
                player.position = row["Position"]

            # Convert the player's statistics
            stats_data = {database_field: convert_value(database_field, row[csv_column]) 
                for csv_column, database_field in COLUMN_MAPPING.items()}

            validation_errors = validate_player_statistics(stats_data, row["Player"])

            if validation_errors:
                invalid_records += 1
                continue

            valid_records += 1

            # Check whether statistics already exist
            statistics = session.query(PlayerStatistics).filter_by(player_id=player.id, team_id=team.id, competition_id=competition.id, season_id=season.id).first()

            if statistics:
                # Update existing statistics
                for field, value in stats_data.items():
                    setattr(statistics, field, value)

            else:
                # Create a new statistics record
                statistics = PlayerStatistics(player_id=player.id, team_id=team.id, competition_id=competition.id, season_id=season.id, **stats_data)

                session.add(statistics)

    print("Player statistics imported successfully!")

    # Verify the total number of records
    with SessionLocal() as session:
        total_records = session.query(PlayerStatistics).count()

    print(f"\nValidation summary:")
    print(f"Valid records: {valid_records}")
    print(f"Invalid records skipped: {invalid_records}")
    print("Total statistics records:", total_records)


if __name__ == "__main__":
    import_player_statistics()
