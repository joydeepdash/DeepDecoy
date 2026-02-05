from pydantic import BaseModel

class IncomingMessage(BaseModel):
    session_id: str
    message: str
    callback_url: str
