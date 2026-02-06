from openai import AsyncOpenAI
import os
from core.config import (
    LLM_MODEL_INTEL,
    LLM_MODEL_RESPONSE,
    TEMPERATURE_INTEL,
    TEMPERATURE_RESPONSE
)

def get_client():
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def call_llm(system_prompt, user_prompt, mode="intel"):

    client = get_client()


    model = LLM_MODEL_INTEL
    temperature = TEMPERATURE_INTEL

    if mode == "response":
        model = LLM_MODEL_RESPONSE
        temperature = TEMPERATURE_RESPONSE

    # Only enforce JSON mode for strategy + intel agents
    kwargs = {}

    if mode != "response":
        kwargs["response_format"] = {"type": "json_object"}

    response = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs
    )

    return response.choices[0].message.content
