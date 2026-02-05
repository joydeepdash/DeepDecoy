from openai import AsyncOpenAI
from core.config import (
    LLM_MODEL_INTEL,
    LLM_MODEL_RESPONSE,
    TEMPERATURE_INTEL,
    TEMPERATURE_RESPONSE
)

client = AsyncOpenAI()


async def call_llm(system_prompt, user_prompt, mode="intel"):

    model = LLM_MODEL_INTEL
    temperature = TEMPERATURE_INTEL

    if mode == "response":
        model = LLM_MODEL_RESPONSE
        temperature = TEMPERATURE_RESPONSE

    response = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content

