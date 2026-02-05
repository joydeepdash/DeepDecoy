from models.session import SessionState

SESSIONS = {}

def get_session(session_id: str) -> SessionState:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = SessionState(session_id=session_id)
    return SESSIONS[session_id]
