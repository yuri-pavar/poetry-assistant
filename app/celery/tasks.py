# from app.celery.worker import celery_app
from app.celery import celery_app
from app.core.config import SYSTEM_PROMPT, USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN
from app.core.pipeline import get_pipeline
# from app.core.generate_vllm import async_generate
from app.core.generate_vllm import generate_sync
import asyncio

pipeline = get_pipeline()
preprocessor, rag_svc, ctx_svc = pipeline

# @celery_app.task(name="app.celery.tasks.generate_poetry_task")
# def generate_poetry_task(query: str):
#     async def inner():
#         print("[DEBUG] START")
#         ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
#         print("[DEBUG] NER: ", ner)
#         if not ner.get("is_direct"):
#             keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
#             ner["keywords"] = keywords
#         print("[DEBUG] NER+keywords: ", ner)
#         context = ctx_svc.prepare_context(query, ner)
#         print("[DEBUG] context: ", context)
#         prompt = USER_PROMPT_MAIN.format(context=context, query=query)
#         print("[DEBUG] prompt: ", prompt)
#         response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#         print("[DEBUG] response: ", response)
#         return {"query": query, "response": response}

#     return asyncio.run(inner())




# from celery import shared_task
# import asyncio

# @shared_task(name="app.celery.tasks.generate_poetry_task")
# def generate_poetry_task(query: str):
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(run_generate(query))

# async def run_generate(query: str):
#     print("[DEBUG] START")

#     ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
#     print("[DEBUG] NER:", ner)

#     if not ner.get("is_direct"):
#         keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
#         print("[DEBUG] Keywords:", keywords)
#         ner["keywords"] = keywords

#     print("[DEBUG] NER+keywords:", ner)
#     context = ctx_svc.prepare_context(query, ner)
#     print("[DEBUG] context:", context[:300])

#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)
#     print("[DEBUG] prompt:", prompt[:500])

#     response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#     print("[DEBUG] response:", response[:500])

#     return {"query": query, "response": response}



# from app.celery import celery_app
# from app.core.config import SYSTEM_PROMPT, USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN
# from app.core.pipeline import get_pipeline
# from app.core.generate_vllm import async_generate
# import asyncio

# pipeline = get_pipeline()
# preprocessor, rag_svc, ctx_svc = pipeline

# @celery_app.task(name="app.celery.tasks.generate_poetry_task")
# def generate_poetry_task(query: str):
#     print("[CELERY] Task started")
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(run_generate(query))

# async def run_generate(query: str):
#     print("[DEBUG] START")
#     ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
#     print("[DEBUG] NER:", ner)

#     if not ner.get("is_direct"):
#         keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
#         print("[DEBUG] Keywords:", keywords)
#         ner["keywords"] = keywords

#     print("[DEBUG] NER+keywords:", ner)
#     context = ctx_svc.prepare_context(query, ner)
#     print("[DEBUG] context:", context[:300])

#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)
#     print("[DEBUG] prompt:", prompt[:500])

#     response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#     print("[DEBUG] response:", response[:500])

#     return {"query": query, "response": response}



@celery_app.task(name="app.celery.tasks.generate_poetry_task")
def generate_poetry_task(query: str):
    print("[DEBUG] START")
    ner = preprocessor.get_query_ner(query, USER_PROMPT_NER)
    print("[DEBUG] NER: ", ner)
    if not ner.get("is_direct"):
        keywords = preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        ner["keywords"] = keywords
    print("[DEBUG] NER+keywords: ", ner)
    context = ctx_svc.prepare_context(query, ner)
    print("[DEBUG] context: ", context)
    prompt = USER_PROMPT_MAIN.format(context=context, query=query)
    print("[DEBUG] prompt: ", prompt)
    response = generate_sync(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
    print("[DEBUG] response: ", response)
    
    return {"query": query, "response": response}
