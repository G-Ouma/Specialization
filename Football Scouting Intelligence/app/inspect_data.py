import pandas as pd
from pathlib import Path


# Locate project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
EVENTS_FILE = (PROJECT_DIR / "data" / "raw" / "match_events_export(3).csv")

# Original Equity FC dataset (historical sample)
EQUITY_PLAYERS_FILE = (PROJECT_DIR / "data" / "raw" / "Equity FC 2025-26 Player Analysis with Per 90.csv")

# New 20-team NSL dataset (primary dataset)
PLAYERS_FILE = (PROJECT_DIR / "data" / "raw" / "nsl_2025_26_20_teams_raw.csv")

# Processed dataset paths
EQUITY_OUTPUT_FILE = (PROJECT_DIR / "data" / "processed" / "equity_fc_players_cleaned.csv")

OUTPUT_FILE = (PROJECT_DIR / "data" / "processed" / "nsl_2025_26_players_cleaned.csv")


def inspect_datasets():
    """Load and inspect the original datasets."""

    events_df = pd.read_csv(EVENTS_FILE)
    players_df = pd.read_csv(PLAYERS_FILE)

    print("Datasets loaded successfully!")

    print("\n--- Dataset Dimensions ---")
    print(f"Match events: {events_df.shape}")
    print(f"Player statistics: {players_df.shape}")

    print("\n--- Match Events Columns ---")
    print(events_df.columns.tolist())

    print("\n--- Player Statistics Columns ---")
    print(players_df.columns.tolist())


def clean_player_dataset(input_file, output_file, dataset_name):
    """Clean and save a player statistics dataset."""

    players_df = pd.read_csv(input_file)

    print(f"\n--- Cleaning {dataset_name} ---")

    # Check player records
    valid_players = players_df["Player"].notna().sum()

    print(f"Total rows: {len(players_df)}")
    print(f"Valid player records: {valid_players}")
    print(f"Blank rows: {len(players_df) - valid_players}")

    # Remove rows without player names
    players_df = players_df.dropna(subset=["Player"]).copy()

    # Convert percentage columns to numeric values
    percentage_columns = ["Pass Accuracy %", "Tackle Success Rate %", "Cross Accuracy %", "Aerial Duels %"]

    for column in percentage_columns:
        players_df[column] = pd.to_numeric(players_df[column].astype("string").str.replace("%", "", regex=False), errors="raise")

    # Check duplicate player records
    duplicate_players = players_df[players_df.duplicated(subset=["Player", "Team"], keep=False)]

    print("\n--- Duplicate Player Check ---")

    if duplicate_players.empty:
        print("No duplicate player-team records found.")
    else:
        print(duplicate_players[["Player", "Team", "Position"]])

    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned dataset
    players_df.to_csv(output_file, index=False)

    print(f"\nCleaned dataset saved to: {output_file}")

    # Analyse player distribution
    print("\n--- Players by Position ---")
    print(players_df["Position"].value_counts())

    # Analyse team distribution if Team column exists
    if "Team" in players_df.columns:
        print("\n--- Players by Team ---")
        print(players_df["Team"].value_counts())

    return players_df


if __name__ == "__main__":
    inspect_datasets()

    # Clean the primary 20-team NSL dataset
    clean_player_dataset(PLAYERS_FILE, OUTPUT_FILE, "20-Team NSL Dataset")

    # Clean the original Equity FC dataset
    if EQUITY_PLAYERS_FILE.exists():
        clean_player_dataset(EQUITY_PLAYERS_FILE, EQUITY_OUTPUT_FILE, "Equity FC Historical Dataset")
    else:
        print("\nOriginal Equity FC dataset not found. Skipping historical dataset.")
