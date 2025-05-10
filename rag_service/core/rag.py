import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from rag_service.core.config import CHROMA_DIR


class RAGService:
    def __init__(self, embed_model, rerank_model, data, persist_directory=CHROMA_DIR):
        self.embed_model = embed_model
        self.rerank_model = rerank_model
        self.persist_directory = persist_directory
        self.ini_data = data
        self.db = None

    def load_db(self):
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            print("[RAGService] Loading existing ChromaDB from disk...")
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embed_model
            )
        else:
            print("[RAGService] No existing DB found at path: ", self.persist_directory)
            self.db = None

    def create_from_data(
        self,
        metadata_cols,
        txt_col,
        rag_separators=["\n\n", "\n", ".", " ", ""],
        prefix_document='search_document: ',
        chunk_size=300,
        chunk_overlap=25
    ):
        all_cols = [txt_col] + metadata_cols
        data = self.ini_data[all_cols]

        print("[RAGService] Creating new ChromaDB...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=rag_separators
        )

        docs = []
        for row in data.values:
            text = row[0]
            metadata_vals = [row[data.columns.get_loc(col)] for col in metadata_cols]
            chs = splitter.split_text(text)
            for ch in chs:
                doc = Document(
                    page_content=f"{prefix_document}{ch.strip()}",
                    metadata=dict(zip(metadata_cols, metadata_vals))
                )
                docs.append(doc)

        self.db = Chroma.from_documents(
            documents=docs,
            embedding=self.embed_model,
            persist_directory=self.persist_directory
        )
        print("[RAGService] New DB created and saved.")

    def _rerank(self, query, results):
      to_rerank = [[query, res.page_content.replace('search_document: ', '') ] for res in results]
      ranks = self.rerank_model.compute_score(to_rerank, normalize=True)
      reranked = sorted(zip(results, ranks), key=lambda x: -x[1])

      return [i[0] for i in reranked]

    def search(self, ini_query, query, prefix_query='search_query: ', method="similarity", k=20, filters=None, rerank=True, rerank_k=5):
        if self.db is None:
            raise ValueError("Database is not loaded. Please create or load a database first.")

        final_query = f'{prefix_query}{query}'
        if method == "similarity":
            if filters:
                results = self.db.similarity_search(final_query, k=k, filter=filters)
            else:
                results = self.db.similarity_search(final_query, k=k)
        elif method == "marginal":
            if filters:
                results = self.db.max_marginal_relevance_search(final_query, k=k, filter=filters)
            else:
                results = self.db.max_marginal_relevance_search(final_query, k=k)
        else:
            raise ValueError(f"Unknown search method: {method}")

        if rerank:
          results = self._rerank(f"Запрос: {ini_query}. Образы: {query}", results)
          results = results[:rerank_k]

        return results
