from fastapi import FastAPI
from rag_service.core.pipeline import get_pipeline
from rag_service.models.schemas import RagQuery
from rag_service.core.context_constructor import ContextConstructor
from rag_service.core.config import CHROMA_DIR_QUOTE


app = FastAPI(title="RAG Service")

rag, cntx = get_pipeline()


@app.post("/get_context")
def build_context(query: RagQuery):
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
