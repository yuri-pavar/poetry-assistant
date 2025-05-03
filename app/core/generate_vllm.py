import httpx
import os
from config import VLLM_API_URL, MODEL_NAME


async def async_generate(prompt: str, system_prompt: str = "", max_tokens: int = 512, temperature: float = 0.7) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(VLLM_API_URL, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Ошибка генерации]: {str(e)}"