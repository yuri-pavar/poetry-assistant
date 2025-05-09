from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "russianPoetryWithTheme_deduped.csv"
CHROMA_DIR = str(BASE_DIR / "data" / "chroma_dir2")

EMBED_MODEL_NAME = "sergeyzh/BERTA"
RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"

AUTHORS_COL = 'author'
POEMS_COL = 'name'
TXT_COL = 'text'

RAG_METADATA_COLS = ['date_to', 'author', 'name']
RAG_TXT_COL = 'text'
RAG_SEARCH_METHOD = 'marginal'