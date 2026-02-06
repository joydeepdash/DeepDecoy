import os
from dotenv import load_dotenv


load_dotenv()

# ---------- MODELS ----------

# Fast reasoning model (strategy + intel planning)
LLM_MODEL_INTEL = os.getenv(
    "LLM_MODEL_INTEL",
    "gpt-4o-mini"
)

# Response generation model
LLM_MODEL_RESPONSE = os.getenv(
    "LLM_MODEL_RESPONSE",
    "gpt-4o-mini"
)

# ---------- TEMPERATURES ----------

# Deterministic reasoning
TEMPERATURE_INTEL = 0.2

# Natural conversational response
TEMPERATURE_RESPONSE = 0.6

# ---------- GENERATION LIMITS ----------

MAX_TOKENS_INTEL = 300
MAX_TOKENS_RESPONSE = 500

def get_api_key():
    key = os.getenv("API_KEY")
    if not key:
        raise RuntimeError("API_KEY not set")
    return key.strip()


FINAL_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
#FINAL_CALLBACK_URL = "http://127.0.0.1:8000/test-callback"


