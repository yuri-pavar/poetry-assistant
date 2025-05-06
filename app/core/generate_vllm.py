import httpx
import os
from app.core.config import VLLM_API_URL, MODEL_NAME, SYSTEM_PROMPT


# def generate_sync(prompt: str, system_prompt: str, max_tokens: int = 400, temperature: float = 0.7, top_p: float = 0.9) -> str:
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "model": "t-tech/T-lite-it-1.0",  # или другой
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt}
#         ],
#         "max_tokens": max_tokens,
#         "temperature": temperature,
#         "top_p": top_p
#     }

#     try:
#         response = httpx.post(VLLM_API_URL, json=payload, timeout=60)
#         response.raise_for_status()
#         result = response.json()
#         return result["choices"][0]["message"]["content"]
#     except Exception as e:
#         print(f"[generate_sync] Ошибка запроса к vLLM: {e}")
#         return ""


async def async_generate(prompt: str, system_prompt: str = SYSTEM_PROMPT, max_tokens: int = 512, temperature: float = 0.7, top_p: float = 0.9) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature, 
        "top_p": top_p
    }
    print("[DEBUG] Payload:", payload)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(VLLM_API_URL, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Ошибка генерации]: {str(e)}"