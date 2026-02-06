from core.llm import call_llm
import json


SYSTEM_PROMPT = """
You are an intelligence planning agent in a scam honeypot system.

Your task:
- Decide what useful information is still missing.
- If sufficient intelligence already exists or the scammer repeats information,
return a low priority goal suggesting conversation wind-down.
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
    
    return json.loads(result)
