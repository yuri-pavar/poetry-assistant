# from app.celery.worker import celery_app
from app.celery import celery_app
from app.core.config import SYSTEM_PROMPT, USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN
from app.core.pipeline import get_pipeline
from app.core.generate_vllm import async_generate
import asyncio

pipeline = get_pipeline()
preprocessor, rag_svc, ctx_svc = pipeline

@celery_app.task(name="app.celery.tasks.generate_poetry_task")
def generate_poetry_task(query: str):
    async def inner():
        ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
        if not ner.get("is_direct"):
            keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
            ner["keywords"] = keywords
        context = ctx_svc.prepare_context(query, ner)
        prompt = USER_PROMPT_MAIN.format(context=context, query=query)
        response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
        return {"query": query, "response": response}

    return asyncio.run(inner())
