from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal

from app.queries import search_players, count_players, get_dashboard_stats, get_player_profile
from app.queries import compare_players
from app.queries import get_player_leaderboard

from app.schemas import PlayerResponse, PlayerProfileResponse


app = FastAPI(
    title="Football Scouting Intelligence API",
    description="API for searching, comparing and analysing football players.",
    version="1.0.0"
)


app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5500"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def get_session_factory():
    return SessionLocal


@app.get("/")
def home():
    return {"message": "Football Scouting Intelligence API is running!"}


@app.get("/players", response_model=list[PlayerResponse])
def get_players(
    name: str | None = None,
    position: str | None = None,
    minimum_goals: int | None = Query(default=None, ge=0),
    minimum_assists: int | None = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session_factory=Depends(get_session_factory)
):
    results = search_players(
        name=name,
        position=position,
        minimum_goals=minimum_goals,
        minimum_assists=minimum_assists,
        skip=skip,
        limit=limit,
        session_factory=session_factory
    )

    return [
        {
            "name": player.name,
            "position": player.position, 
            **{column: getattr(statistics, column) for column in PlayerResponse.model_fields if column not in ("name", "position")}
        } for player, statistics in results
    ]


@app.get("/players/count")
def get_players_count(name:str|None=None, position:str|None=None, minimum_goals:int|None=Query(default=None, ge=0), minimum_assists:int|None=Query(default=None, ge=0)):
    return {"total": count_players(name=name, position=position, minimum_goals=minimum_goals, minimum_assists=minimum_assists)}


@app.get("/dashboard")
def dashboard():
    return get_dashboard_stats()


@app.get(
    "/players/compare",
    responses={
        400: {"description": "Invalid or ambiguous player selection"},
        404: {"description": "Player not found"},
    },
)
def compare_two_players(player1:str, player2:str, mode:str="combined", competition:str|None=None, season:str|None=None, team:str|None=None, session_factory=Depends(get_session_factory)):
    try:
        results = compare_players(player1, player2, mode=mode, competition=competition, season=season, team=team, session_factory=session_factory)

        return [
            {
                "name": player.name,
                "position": player.position,
                **statistics
            }
            for player, statistics in results
        ]

    except ValueError as error:
        message = str(error)

        if message.startswith("No player found"):
            status_code = 404
        else:
            status_code = 400

        raise HTTPException(status_code=status_code, detail=message)


@app.get("/players/{player_name}/profile", response_model=PlayerProfileResponse)
def player_profile(player_name: str):
    profile = get_player_profile(player_name)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found."
        )

    return profile


@app.get("/players/leaderboard")
def player_leaderboard(statistic: str = "goals", limit: int = Query(default=10, ge=1, le=100), session_factory=Depends(get_session_factory)
):
    try:
        results = get_player_leaderboard(statistic=statistic, limit=limit, session_factory=session_factory)

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
        raise HTTPException(status_code=400, detail=str(error))