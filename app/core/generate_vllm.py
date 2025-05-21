import requests
import os
from app.core.config import VLLM_API_URL, MODEL_NAME, SYSTEM_PROMPT, VLLM_API_LORA_UPLOAD_URL


def generate_sync(prompt: str, use_lora=None, system_prompt: str = SYSTEM_PROMPT, max_tokens: int = 1024, temperature: float = 0.7, top_p: float = 0.9) -> str:
    headers = {"Content-Type": "application/json"}
    print('[LORA] generate_sync.use_lora', use_lora)
    if use_lora:
        headers['x-lora-adapter'] = use_lora
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
        # response = requests.post(VLLM_API_URL, json=payload, timeout=60)
        response = requests.post(VLLM_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        fin_res = result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[generate_sync] Ошибка запроса к vLLM: {e}")
        fin_res = ""
    
    if "." in fin_res:
        fin_res = fin_res.rsplit(".", 1)[0] + "."

    return fin_res


def load_lora(lora_name: str, lora_path: str) -> bool:
    try:
        payload = {"lora_name": lora_name, "lora_path": lora_path}
        # resp = requests.post(f"{VLLM_API_URL}/load_lora_adapter", json=payload, timeout=10)
        resp = requests.post(f"{VLLM_API_LORA_UPLOAD_URL}/load_lora_adapter", json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"[load_lora] Ошибка: {e}")
        return False


def unload_lora(lora_name: str) -> bool:
    try:
        payload = {"lora_name": lora_name}
        # resp = requests.post(f"{VLLM_API_URL}/unload_lora_adapter", json=payload, timeout=10)
        resp = requests.post(f"{VLLM_API_LORA_UPLOAD_URL}/unload_lora_adapter", json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"[unload_lora] Ошибка: {e}")
        return False