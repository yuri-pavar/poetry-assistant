from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "russianPoetryWithTheme_deduped.csv"

# CHROMA_DIR = str(BASE_DIR / "data" / "chroma_dir2")
# EMBED_MODEL_NAME = "sergeyzh/BERTA"
# RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"

CHROMA_DIR = str(BASE_DIR / "data" / "chroma_FRIDA_750_25")
CHROMA_DIR_QUOTE = str(BASE_DIR / "data" / "chroma_FRIDA_300_25")

EMBED_MODEL_NAME = "ai-forever/FRIDA"
RERANK_MODEL_NAME = "Alibaba-NLP/gte-multilingual-reranker-base"

AUTHORS_COL = 'author'
POEMS_COL = 'name'
TXT_COL = 'text'

RAG_METADATA_COLS = ['date_to', 'author', 'name']
RAG_TXT_COL = 'text'
RAG_SEARCH_METHOD = 'marginal'