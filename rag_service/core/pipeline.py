import os
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
import torch
from rag_service.core.config import DATA_PATH, EMBED_MODEL_NAME, AUTHORS_COL, POEMS_COL, RAG_METADATA_COLS, RAG_TXT_COL, TXT_COL, CHROMA_DIR, RERANK_MODEL_NAME
from rag_service.core.rag import RAGService
from rag_service.core.context_constructor import ContextConstructor
from FlagEmbedding import FlagReranker


device = "cuda" if torch.cuda.is_available() else "cpu"

def get_pipeline():

    data = pd.read_csv(DATA_PATH)
    
    embed_model = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL_NAME,
        model_kwargs={"device": device}
    )

    reranker = FlagReranker(RERANK_MODEL_NAME, use_fp16=True, device=device)

    rag = RAGService(embed_model, reranker, data)

    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        rag.load_db()
    else:
        rag.create_from_data(
            metadata_cols=RAG_METADATA_COLS,
            txt_col=RAG_TXT_COL
        )

    cntx = ContextConstructor(
        data=data,
        authors_col=AUTHORS_COL,
        poems_col=POEMS_COL,
        txt_col=TXT_COL,
        rag_svc=rag
    )

    return rag, cntx