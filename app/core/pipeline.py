import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain.embeddings import HuggingFaceEmbeddings
# from app.core.config import DATA_PATH, MODEL_NAME, EMBED_MODEL
# from app.preprocessor import Preprocessor
# from app.rag import RAGService
# from app.context import ContextConstructor
from config import DATA_PATH, MODEL_NAME, EMBED_MODEL, AUTHORS_COL, POEMS_COL, RAG_METADATA_COLS, RAG_TXT_COL, TXT_COL
from preprocessor import Preprocessor
from rag import RAGService
from context_constructor import ContextConstructor


_pipeline = None


def get_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    data = pd.read_csv(DATA_PATH)

    quant_config = BitsAndBytesConfig(load_in_8bit=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True
    )
    model.eval()

    embed_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    preproc = Preprocessor(
        model=model,
        tokenizer=tokenizer,
        data=data,
        authors_col=AUTHORS_COL,
        poems_col=POEMS_COL
    )

    rag = RAGService(embed_model, data)
    rag.create_from_data(
        metadata_cols = RAG_METADATA_COLS,
        txt_col = RAG_TXT_COL
    )

    cntx = ContextConstructor(
        data=data,
        authors_col=AUTHORS_COL,
        poems_col=POEMS_COL,
        txt_col=TXT_COL,
        rag_svc=rag,
    )
    _pipeline = (preproc, rag, cntx)

    return _pipeline