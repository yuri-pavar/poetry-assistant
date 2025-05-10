import requests
import os
from app.core.config import VLLM_API_URL, MODEL_NAME, SYSTEM_PROMPT


def generate_sync(prompt: str, system_prompt: str = SYSTEM_PROMPT, max_tokens: int = 1024, temperature: float = 0.7, top_p: float = 0.9) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    try:
        response = requests.post(VLLM_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        fin_res = result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[generate_sync] Ошибка запроса к vLLM: {e}")
        fin_res = ""
    
    if "." in fin_res:
        fin_res = fin_res.rsplit(".", 1)[0] + "."

    return fin_res