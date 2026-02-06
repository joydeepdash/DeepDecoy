import json
from core.llm import call_llm
from models.strategy import StrategyDecision
from models.session import StrategyState


SYSTEM_PROMPT = """
You are an autonomous scam engagement controller.

Based on the conversation history and extracted intelligence decide:

1. Next strategy state:
   - INIT
   - ENGAGE
   - EXTRACT
   - DELAY
   - TERMINATE

2. scam_confidence (0 to 1)
3. intel_score (0 to 1)
4. engagement_score (0 to 1)

Rules:
- If scam confidence is low → stay in INIT or ENGAGE
- If scam confidence high and intel incomplete → ENGAGE
- If useful intelligence has started being collected → EXTRACT
- If enough intelligence is gathered (multiple fields collected) → DELAY
- If conversation exhausted or scammer stops providing useful information → TERMINATE

Important:
- If at least two distinct intelligence categories are collected, prefer EXTRACT or DELAY over ENGAGE.
- Do not remain in ENGAGE indefinitely once intelligence is accumulating.

Termination guidance:
- If multiple intelligence categories are already collected AND
  recent messages do not introduce new intelligence,
  prefer TERMINATE.
- Do not remain in EXTRACT once payment method, contact info,
  or link has already been obtained unless new intelligence appears.


Return JSON only. The JSON keys MUST exactly match:
next_state, scam_confidence, intel_score, engagement_score, reasoning
"""


async def decide_next_state(session):
    """
    Uses LLM to determine next strategy state.
    """

    # Last few turns for context
    history_text = "\n".join(
        [f"{t['role']}: {t['content']}" for t in session.history[-6:]]
    )

    # NEW: provide extracted intelligence explicitly
    intel_summary = f"""
Extracted intelligence so far:
{session.extracted_intel}
"""

    user_prompt = f"""
Conversation history:
{history_text}

{intel_summary}
"""

    result = await call_llm(
        SYSTEM_PROMPT,
        user_prompt
    )

    data = json.loads(result)

    # normalize common LLM mistakes
    if "next_strategy_state" in data:
        data["next_state"] = data.pop("next_strategy_state")

    # normalize enum casing
    if "next_state" in data:
        data["next_state"] = data["next_state"].lower()

    if "reasoning" not in data:
        data["reasoning"] = "LLM reasoning not provided"

    decision = StrategyDecision(**data)

    return decision
