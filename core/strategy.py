from core.llm import call_llm
from models.strategy import StrategyDecision
from models.session import StrategyState


SYSTEM_PROMPT = """
You are an autonomous scam engagement controller.

Based on the conversation history decide:

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
- If scam confidence high and intel incomplete → EXTRACT
- If enough intel gathered → DELAY
- If conversation exhausted → TERMINATE

Return JSON only.
"""


async def decide_next_state(session):
    """
    Uses LLM to determine next strategy state.
    """

    history_text = "\n".join(
        [f"{t['role']}: {t['content']}" for t in session.history[-6:]]
    )

    result = await call_llm(
        SYSTEM_PROMPT,
        history_text
    )

    decision = StrategyDecision(**result)

    return decision
