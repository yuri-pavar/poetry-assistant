import requests
from app.core.config import RAG_SERVICE_URL

def get_context_from_rag(query: str, filters: dict, method: str = "marginal", k: int = 5):
    payload = {
        "query": query,
        "filters": filters,
        "method": method,
        "k": k
    }
    try:
        res = requests.post(f"{RAG_SERVICE_URL}/get_context", json=payload, timeout=60)
        res.raise_for_status()
        return res.json()["context"]
    except Exception as e:
        print(f"[rag_client] Ошибка при запросе к RAG: {e}")
        return ""
