import os

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
