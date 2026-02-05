from pydantic import BaseModel
from typing import List
from enum import Enum

class ChatTurn(BaseModel):
    role: str
    content: str

class SessionState(BaseModel):
    session_id: str
    history: List[ChatTurn] = []
    extracted_intel: dict = {}

class StrategyState(str, Enum):
    INIT = "init"
    ENGAGE = "engage"
    EXTRACT = "extract"
    DELAY = "delay"
    TERMINATE = "terminate"

class SessionState(BaseModel):
    session_id: str
    history: List[ChatTurn] = []
    extracted_intel: dict = {}
    state: StrategyState = StrategyState.INIT
    turns: int = 0
