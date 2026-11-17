
import pandas as pd
from pathlib import Path


# Locate project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
EVENTS_FILE = (
    PROJECT_DIR / "data" / "raw" / "match_events_export(3).csv"
)

PLAYERS_FILE = (
    PROJECT_DIR / "data" / "raw"
    / "Equity FC 2025-26 Player Analysis with Per 90.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed" / "players_cleaned.csv"
)


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


def clean_player_dataset():
    """Clean and save the player statistics dataset."""

    players_df = pd.read_csv(PLAYERS_FILE)

    # Count valid player records
    valid_players = players_df["Player"].notna().sum()

    print("\n--- Player Record Check ---")
    print(f"Total rows: {len(players_df)}")
    print(f"Valid player records: {valid_players}")
    print(f"Blank rows: {len(players_df) - valid_players}")

    # Remove rows without player names
    players_df = players_df.dropna(
        subset=["Player"]
    ).copy()

    # Convert percentage columns to numeric values
    percentage_columns = [
        "Pass Accuracy %",
        "Tackle Success Rate %",
        "Cross Accuracy %",
        "Aerial Duels %"
    ]

    for column in percentage_columns:
        players_df[column] = pd.to_numeric(
            players_df[column]
            .astype("string")
            .str.replace("%", "", regex=False),
            errors="raise"
        )

    # Check for duplicate player records
    duplicate_players = players_df[
        players_df.duplicated(
            subset=["Player"],
            keep=False
        )
    ]

    print("\n--- Duplicate Player Check ---")

    if duplicate_players.empty:
        print("No duplicate player records found.")
    else:
        print(duplicate_players[["Player", "Position"]])

    # Save cleaned dataset
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    players_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nCleaned dataset saved to: {OUTPUT_FILE}")

    # Analyse player distribution
    print("\n--- Players by Position ---")
    print(players_df["Position"].value_counts())


if __name__ == "__main__":
    inspect_datasets()
    clean_player_dataset()
