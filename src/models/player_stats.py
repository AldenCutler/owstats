from pydantic import BaseModel, Field

class PlayerStats(BaseModel):
    kills: int = Field(..., description="Number of kills")
    deaths: int = Field(..., description="Number of deaths")
    assists: int = Field(..., description="Number of assists")
    damage_dealt: int = Field(..., description="Total damage dealt")
    damage_taken: int = Field(..., description="Total damage taken")
    healing_done: int = Field(..., description="Total healing done")
    hero: str = Field(..., description="Hero played by the player")