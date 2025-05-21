from app.celery import celery_app
from app.core.config import SYSTEM_PROMPT, USER_PROMPT_NER, USER_PROMPT_REWRITING, USER_PROMPT_MAIN, DATA_PATH, AUTHORS_COL, POEMS_COL, USER_PROMPT_POEM
from app.core.generate_vllm import generate_sync, load_lora, unload_lora
from app.core.rag_client import get_context_from_rag
from app.core.preprocessor import Preprocessor
import pandas as pd


data = pd.read_csv(DATA_PATH)

preprocessor = Preprocessor(
        data=data,
        authors_col=AUTHORS_COL,
        poems_col=POEMS_COL
    )

@celery_app.task(name="app.celery.tasks.generate_poetry_task")
def generate_poetry_task(query: str):
    ner = preprocessor.get_query_ner(query, USER_PROMPT_NER)
    if not ner.get("is_direct"):
        keywords = preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        ner["keywords"] = keywords
    print('[NER]', ner)
    context = get_context_from_rag(query, ner, add_metadata=True, qcntx=True)
    print('[CONTEXT]', context)
    prompt = USER_PROMPT_MAIN.format(context=context, query=query)
    response = generate_sync(prompt, system_prompt=SYSTEM_PROMPT)
    
    return {"query": query, "response": response}

@celery_app.task(name="app.celery.tasks.generate_quote_task")
def generate_quote_task(query: str, k: int):
    ner = preprocessor.get_query_ner(query, USER_PROMPT_NER)
    if not ner.get("is_direct"):
        keywords = preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        ner["keywords"] = keywords
    print('[NER]', ner)
    context = get_context_from_rag(query, ner, add_metadata=True, qcntx=False, k=k)
    
    return {"query": query, "response": context}

@celery_app.task(name="app.celery.tasks.generate_new_poem_task")
def generate_new_poem_task(query: str):
    ner = preprocessor.get_query_ner(query, USER_PROMPT_NER)
    if not ner.get("is_direct"):
        keywords = preprocessor.get_query_rewrite(query, USER_PROMPT_REWRITING)
        ner["keywords"] = keywords
    print('[NER]', ner)
    context = get_context_from_rag(query, ner, add_metadata=False, qcntx=True)
    print('[CONTEXT]', context)
    prompt = USER_PROMPT_POEM.format(context=context, query=query)

    if 'Александр Пушкин' in ner.get("authors", []):
        # load_lora('poetry_pushkin', '/app/data/lora-poetry-pushkin')
        lora_name = 'pushkin'
        lora_path = '/app/data/lora-poetry-pushkin'
    else:
        # load_lora('poetry', '/app/data/lora-poetry')
        lora_name = 'poetry'
        lora_path = '/app/data/lora-poetry'
    load_lora(lora_name, lora_path)
    print('[LORA] - load')
    # response = generate_sync(prompt, use_lora='poetry', system_prompt=SYSTEM_PROMPT, max_tokens=400)
    response = generate_sync(prompt, use_lora=lora_name, system_prompt=SYSTEM_PROMPT, max_tokens=400)
    unload_lora(lora_name)
    print('[LORA] - unload')

    return {"query": query, "response": response}
