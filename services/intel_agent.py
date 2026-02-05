from core.llm import call_llm


SYSTEM_PROMPT = """
You are an intelligence planning agent in a scam honeypot system.

Your task:
- Decide what useful information is still missing.
- Suggest the next information-gathering objective.

Examples:
- payment method
- bank details
- phone number
- link or platform used

Return JSON only with:
{
  "goal": "...",
  "next_question_hint": "...",
  "priority": "low|medium|high"
}
"""


async def plan_next_intel(message, state):
    result = await call_llm(
        SYSTEM_PROMPT,
        f"State: {state}\nMessage: {message}"
    )

    return result
