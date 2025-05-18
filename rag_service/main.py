from fastapi import FastAPI
from rag_service.core.pipeline import get_pipeline
from rag_service.models.schemas import RagQuery
from rag_service.core.context_constructor import ContextConstructor
from rag_service.core.config import CHROMA_DIR_QUOTE


app = FastAPI(title="RAG Service")

rag, cntx = get_pipeline()

# rag_main, cntx_main = get_pipeline()
# rag_quote, cntx_quote = get_pipeline(rag_dir=CHROMA_DIR_QUOTE)

@app.post("/get_context")
def build_context(query: RagQuery):
    # print('[RAG_SVC_MAIN - add_metadata]', query.add_metadata)
    print('[RAG_SVC_MAIN - cntx]', query.qcntx)
    # if query.qcntx:
    #     print('[RAG_SVC_MAIN - cntx_main]', query.qcntx)
    #     cntx = cntx_main
    # else:
    #     print('[RAG_SVC_MAIN - cntx_quote]', query.qcntx)
    #     cntx = cntx_quote
    context = cntx.prepare_context(
        query=query.query,
        response={
            "keywords": query.filters.get("keywords", []), 
            "authors": query.filters.get("authors", []), 
            "poems": query.filters.get("poems", []), 
            "is_direct": query.filters.get("is_direct", 0)
        },
        add_metadata=query.add_metadata,
        rag_method=query.method,
        k=query.k
    )
    return {"context": context}
