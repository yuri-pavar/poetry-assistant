# import asyncio
# import httpx

# async def test_vllm():
#     url = "http://localhost:8000/v1/chat/completions"
#     payload = {
#         "model": "t-tech/T-lite-it-1.0",
#         "messages": [
#             {"role": "system", "content": "Ты помощник по русской поэзии."},
#             {"role": "user", "content": "Напиши пару строк о зиме и любви."}
#         ],
#         "max_tokens": 60,
#         "temperature": 0.8
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=payload)
#         response.raise_for_status()
#         print(response.json()["choices"][0]["message"]["content"])

# asyncio.run(test_vllm())


import asyncio
from app.core.pipeline import get_pipeline
from app.core.generate_vllm import async_generate
from app.core.config import USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN, SYSTEM_PROMPT


pipeline = get_pipeline()
preprocessor, rag_svc, ctx_svc = pipeline


async def debug_task(query: str):
    print("[TASK STARTED]")

    ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
    print("[NER]", ner)

    if not ner.get("is_direct"):
        keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        print("[KEYWORDS]", keywords)
        ner["keywords"] = keywords

    print("[BEFORE CONTEXT PREPARE]")
    context = ctx_svc.prepare_context(query, ner)
    print("[CONTEXT]", context)

    prompt = USER_PROMPT_MAIN.format(context=context, query=query)
    print("[PROMPT]", prompt)

    response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
    print("[RESPONSE]", response)

    return {"query": query, "response": response}


if __name__ == "__main__":
    asyncio.run(debug_task("Как Пушкин описывает осень?"))

