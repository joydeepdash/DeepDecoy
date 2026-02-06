import httpx

async def send_callback(callback_url: str, payload: dict):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            await client.post(callback_url, json=payload)
        except Exception as e:
            print("Callback failed:", str(e))
