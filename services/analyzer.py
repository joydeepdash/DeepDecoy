from core.llm import call_llm


SYSTEM_PROMPT = """
You are a scam engagement agent interacting with a suspected scammer.

Your goal depends on the current strategy state:

INIT:
- Be polite and neutral.
- Do not reveal suspicion.
- Keep conversation alive.

ENGAGE:
- Show interest or mild confusion.
- Encourage longer responses.

EXTRACT:
- Ask natural questions to obtain useful details
  such as payment method, contact info, links, or instructions.

DELAY:
- Slow progress naturally.
- Pretend technical issues or misunderstandings.

TERMINATE:
- Politely end conversation without confrontation.

Always respond naturally like a normal user.
"""


async def analyze_message(message: str, state: str, intel_plan: dict):

    prompt = f"""
Current strategy state: {state}

Current intelligence goal:
{intel_plan.get("goal")}

Suggested direction:
{intel_plan.get("next_question_hint")}

Incoming message:
{message}
"""

    result = await call_llm(
        SYSTEM_PROMPT,
        prompt
    )

    return result

