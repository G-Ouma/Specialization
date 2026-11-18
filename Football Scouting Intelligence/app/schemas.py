from pydantic import BaseModel


class PlayerResponse(BaseModel):
    model_config = {
        "from_attributes": True
    }

    name: str
    position: str | None = None

    goals: int | None = None
    assists: int | None = None

    pass_accuracy: float | None = None
    interceptions: int | None = None
    tackles_won: int | None = None
    key_passes: int | None = None
    chances_created: int | None = None
    goals_per_90: float | None = None