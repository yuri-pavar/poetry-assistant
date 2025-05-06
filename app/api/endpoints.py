from fastapi import APIRouter, HTTPException
# from fastapi.concurrency import run_in_threadpool
from app.models.schemas import QueryRequest, Output
# from app.core.pipeline import get_pipeline
from app.core.generate_vllm import async_generate
# from app.core.generate_vllm import generate_sync
from app.core.config import SYSTEM_PROMPT, USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN
from app.core import state


router = APIRouter()

# @router.post("/generate")
# async def generate_poetry(request: QueryRequest):
#     query = request.query

#     preprocessor, rag_svc, ctx_svc = await run_in_threadpool(get_pipeline)
#     ner = await run_in_threadpool(preprocessor.get_query_ner, query, SYSTEM_PROMPT, USER_PROMPT_NER)

#     if not ner.get("is_direct"):
#         keywords = await run_in_threadpool(preprocessor.get_query_rewrite, query, SYSTEM_PROMPT, USER_PROMPT_REWRITING)
#         ner["keywords"] = keywords

#     context = await run_in_threadpool(ctx_svc.prepare_context, query, ner)
#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)

#     response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#     return {"query": query, "response": response}

# @router.post("/generate")
# def generate_poetry(request: QueryRequest):
#     query = request.query

#     preprocessor, rag_svc, ctx_svc = get_pipeline()
#     ner = preprocessor.get_query_ner(query, SYSTEM_PROMPT, USER_PROMPT_NER)

#     if not ner.get("is_direct"):
#         keywords = preprocessor.get_query_rewrite(query, SYSTEM_PROMPT, USER_PROMPT_REWRITING)
#         ner["keywords"] = keywords

#     context = ctx_svc.prepare_context(query, ner)
#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)

#     response = generate_sync(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#     return {"query": query, "response": response}





# @router.post("/generate")
# def generate_poetry(request: QueryRequest):
#     query = request.query

#     preprocessor, rag_svc, ctx_svc = get_pipeline()
#     ner = preprocessor.get_query_ner(query, SYSTEM_PROMPT, USER_PROMPT_NER)

#     if not ner.get("is_direct"):
#         keywords = preprocessor.get_query_rewrite(query, SYSTEM_PROMPT, USER_PROMPT_REWRITING)
#         ner["keywords"] = keywords

#     context = ctx_svc.prepare_context(query, ner)
#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)
#     print(prompt)
#     response = generate_sync(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)

#     return {"query": query, "response": response}


# @router.post("/generate")
# async def generate_poetry(request: QueryRequest):
#     query = request.query

#     preprocessor, rag_svc, ctx_svc = await run_in_threadpool(get_pipeline)
#     ner = await run_in_threadpool(preprocessor.get_query_ner, query, SYSTEM_PROMPT, USER_PROMPT_NER)

#     if not ner.get("is_direct"):
#         keywords = await run_in_threadpool(preprocessor.get_query_rewrite, query, SYSTEM_PROMPT, USER_PROMPT_REWRITING)
#         ner["keywords"] = keywords

#     context = await run_in_threadpool(ctx_svc.prepare_context, query, ner)
#     prompt = USER_PROMPT_MAIN.format(context=context, query=query)

#     response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
#     final_obj = Output(query=query, response=response)

#     # return {"query": query, "response": response}
#     return final_obj


@router.post("/generate")
async def generate_poetry(request: QueryRequest):
    if state.pipeline is None:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    preprocessor, rag_svc, ctx_svc = state.pipeline
    
    query = request.query
    ner = await preprocessor.get_query_ner(query, USER_PROMPT_NER)
    # print(ner)
    if not ner.get("is_direct"):
        keywords = await preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        ner["keywords"] = keywords
    # print(keywords)
    context = ctx_svc.prepare_context(query, ner)
    prompt = USER_PROMPT_MAIN.format(context=context, query=query)
    print(prompt)
    response = await async_generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=400)
    final_obj = Output(query=query, response=response)

    # return {"query": query, "response": response}
    return final_obj