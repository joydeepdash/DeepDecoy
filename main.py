from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Agentic HoneyPot")

app.include_router(router)
