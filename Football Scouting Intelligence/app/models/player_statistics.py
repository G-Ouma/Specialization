from sqlalchemy import ForeignKey, Float, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PlayerStatistics(Base):
    __tablename__ = "player_statistics"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "team_id",
            "competition_id",
            "season_id",
            name="unique_player_season_statistics"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))

    player: Mapped["Player"] = relationship(back_populates="statistics")
    team: Mapped["Team"] = relationship(back_populates="statistics")
    competition: Mapped["Competition"] = relationship(back_populates="statistics")
    season: Mapped["Season"] = relationship(back_populates="statistics")

    # Passing
    passes_complete: Mapped[int | None] = mapped_column(Integer)
    passes_incomplete: Mapped[int | None] = mapped_column(Integer)
    pass_accuracy: Mapped[float | None] = mapped_column(Float)

    # Attacking
    goals: Mapped[int | None] = mapped_column(Integer)
    assists: Mapped[int | None] = mapped_column(Integer)
    shots: Mapped[int | None] = mapped_column(Integer)

    # Discipline
    fouls_committed: Mapped[int | None] = mapped_column(Integer)
    yellow_cards: Mapped[int | None] = mapped_column(Integer)
    red_cards: Mapped[int | None] = mapped_column(Integer)


    # Defensive
    tackles_won: Mapped[int | None] = mapped_column(Integer)
    tackles_lost: Mapped[int | None] = mapped_column(Integer)
    total_tackles: Mapped[int | None] = mapped_column(Integer)
    tackle_success_rate: Mapped[float | None] = mapped_column(Float)

    tackles_won_per_90: Mapped[float | None] = mapped_column(Float)
    tackles_lost_per_90: Mapped[float | None] = mapped_column(Float)

    interceptions: Mapped[int | None] = mapped_column(Integer)
    interceptions_per_90: Mapped[float | None] = mapped_column(Float)

    clearances: Mapped[int | None] = mapped_column(Integer)
    blocks: Mapped[int | None] = mapped_column(Integer)

    # Crossing
    crosses_attempted: Mapped[int | None] = mapped_column(Integer)
    crosses_complete: Mapped[int | None] = mapped_column(Integer)
    cross_accuracy: Mapped[float | None] = mapped_column(Float)

    crosses_attempted_per_90: Mapped[float | None] = mapped_column(Float)
    crosses_complete_per_90: Mapped[float | None] = mapped_column(Float)

    # Ball recovery and possession
    ball_won_opponent_half: Mapped[int | None] = mapped_column(Integer)
    ball_won_own_half: Mapped[int | None] = mapped_column(Integer)
    ball_lost_own_half: Mapped[int | None] = mapped_column(Integer)
    ball_lost_opponent_half: Mapped[int | None] = mapped_column(Integer)

    # Dribbling and penalty-box activity
    dribbles: Mapped[int | None] = mapped_column(Integer)
    box_carries: Mapped[int | None] = mapped_column(Integer)
    box_touches: Mapped[int | None] = mapped_column(Integer)

    # Progressive passing
    progressive_passes_complete: Mapped[int | None] = mapped_column(Integer)
    progressive_passes_incomplete: Mapped[int | None] = mapped_column(Integer)

    # Creativity
    chances_created: Mapped[int | None] = mapped_column(Integer)
    key_passes: Mapped[int | None] = mapped_column(Integer)
    
    # Per-90 performance
    passes_complete_per_90: Mapped[float | None] = mapped_column(Float)
    passes_incomplete_per_90: Mapped[float | None] = mapped_column(Float)

    goals_per_90: Mapped[float | None] = mapped_column(Float)
    assists_per_90: Mapped[float | None] = mapped_column(Float)
    shots_per_90: Mapped[float | None] = mapped_column(Float)
    fouls_committed_per_90: Mapped[float | None] = mapped_column(Float)

    ball_won_opponent_per_90: Mapped[float | None] = mapped_column(Float)
    ball_won_own_per_90: Mapped[float | None] = mapped_column(Float)
    ball_lost_own_per_90: Mapped[float | None] = mapped_column(Float)
    ball_lost_opponent_per_90: Mapped[float | None] = mapped_column(Float)

    dribbles_per_90: Mapped[float | None] = mapped_column(Float)
    box_carries_per_90: Mapped[float | None] = mapped_column(Float)
    box_touches_per_90: Mapped[float | None] = mapped_column(Float)

    progressive_passes_complete_per_90: Mapped[float | None] = mapped_column(Float)
    progressive_passes_incomplete_per_90: Mapped[float | None] = mapped_column(Float)

    # Playing time and appearances
    estimated_minutes: Mapped[float | None] = mapped_column(Float)
    matches: Mapped[int | None] = mapped_column(Integer)
    estimated_starts: Mapped[int | None] = mapped_column(Integer)
    estimated_sub_apps: Mapped[int | None] = mapped_column(Integer)
    estimated_90s: Mapped[float | None] = mapped_column(Float)

    # Aerial duels
    aerial_duels_won: Mapped[int | None] = mapped_column(Integer)
    aerial_duels_total: Mapped[int | None] = mapped_column(Integer)
    aerial_duels_success_rate: Mapped[float | None] = mapped_column(Float)
