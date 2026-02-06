from pydantic import BaseModel
from typing import List, Dict, Any
from enum import Enum


class StrategyState(str, Enum):
    INIT = "init"
    ENGAGE = "engage"
    EXTRACT = "extract"
    DELAY = "delay"
    TERMINATE = "terminate"


class ChatTurn(BaseModel):
    role: str
    content: str


class SessionState(BaseModel):
    session_id: str
    history: List[dict] = []
    extracted_intel: Dict[str, Any] = {}
    state: StrategyState = StrategyState.INIT
    turns: int = 0
    last_scores: Dict[str, float] = {}

    # ✅ prevents duplicate callbacks after termination
    callback_sent: bool = False
