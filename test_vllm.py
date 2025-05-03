import asyncio
import httpx

async def test_vllm():
    url = "http://localhost:8000/v1/chat/completions"
    payload = {
        "model": "t-tech/T-lite-it-1.0",
        "messages": [
            {"role": "system", "content": "Ты помощник по русской поэзии."},
            {"role": "user", "content": "Напиши пару строк о зиме и любви."}
        ],
        "max_tokens": 60,
        "temperature": 0.8
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        print(response.json()["choices"][0]["message"]["content"])

asyncio.run(test_vllm())
