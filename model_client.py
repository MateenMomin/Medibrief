import httpx

MODEL_API_URL = "https://semirealistic-nancy-indefectible.ngrok-free.dev/summarize"

async def get_summary(text: str):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                MODEL_API_URL,
                json={"text": text}
            )
            data = response.json()
            return data.get("summary", "Error from model")
    except Exception:
        return "Model service is currently unavailable"
        
        