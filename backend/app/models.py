from pydantic import BaseModel

class SafetyFactors(BaseModel):
    crime: int
    lighting: int

class SafetyScore(BaseModel):
    score: int
    band: str
    factors: SafetyFactors
