from pydantic import BaseModel
from models.session import StrategyState

class StrategyDecision(BaseModel):
    next_state: StrategyState
    scam_confidence: float
    intel_score: float
    engagement_score: float
    reasoning: str
