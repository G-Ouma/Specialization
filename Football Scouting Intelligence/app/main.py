from fastapi import FastAPI, HTTPException, Depends
from app.database import SessionLocal

from app.queries import search_players
from app.queries import compare_players
from app.queries import get_player_leaderboard

from app.schemas import PlayerResponse


app = FastAPI(
    title="Football Scouting Intelligence API",
    description="API for searching, comparing and analysing football players.",
    version="1.0.0"
)


def get_session_factory():
    return SessionLocal


@app.get("/")
def home():
    return {
        "message": "Football Scouting Intelligence API is running!"
    }


@app.get("/players", response_model=list[PlayerResponse])
def get_players(
    name: str | None = None,
    position: str | None = None,
    minimum_goals: int | None = None,
    minimum_assists: int | None = None,
    session_factory=Depends(get_session_factory)
):
    results = search_players(
        name=name,
        position=position,
        minimum_goals=minimum_goals,
        minimum_assists=minimum_assists,
        session_factory=session_factory
    )

    return [
        {
            "name": player.name,
            "position": player.position,
            **{
                column: getattr(statistics, column)
                for column in PlayerResponse.model_fields
                if column not in ("name", "position")
            }
        }
        for player, statistics in results
    ]



@app.get(
    "/players/compare",
    responses={
        400: {"description": "Invalid or ambiguous player selection"},
        404: {"description": "Player not found"},
    },
)
def compare_two_players(
    player1: str,
    player2: str,
    session_factory=Depends(get_session_factory)
):
    try:
        results = compare_players(player1, player2, session_factory=session_factory)

        return [
            {
                "name": player.name,
                "position": player.position,
                "goals": statistics.goals,
                "assists": statistics.assists,
                "pass_accuracy": statistics.pass_accuracy,
                "interceptions": statistics.interceptions,
                "tackles_won": statistics.tackles_won
            }
            for player, statistics in results
        ]

    except ValueError as error:
        message = str(error)

        if message.startswith("No player found"):
            status_code = 404
        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=message
        )


@app.get("/players/leaderboard")
def player_leaderboard(
    statistic: str = "goals",
    limit: int = 10,
    session_factory=Depends(get_session_factory)
):
    try:
        results = get_player_leaderboard(
            statistic=statistic,
            limit=limit,
            session_factory=session_factory
        )

        return [
            {
                "name": player.name,
                "position": player.position,
                "statistic": statistic,
                "value": getattr(statistics, statistic)
            }
            for player, statistics in results
        ]

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )