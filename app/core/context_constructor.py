import re
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ContextConstructor:
    def __init__(
        self,
        data,
        authors_col,
        poems_col,
        txt_col,
        rag_svc,
        max_tokens=2000,
        chunk_overlap=0,
        separators=["\n\n", "\n", ".", " ", ""]
    ):
        self.data_ini = data
        self.authors_col = authors_col
        self.poems_col = poems_col
        self.txt_col = txt_col
        self.rag_svc = rag_svc
        self.max_tokens = max_tokens
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_tokens * 4,  # ~4 chars per token
            chunk_overlap=chunk_overlap,
            separators=separators
        )
        self.data_ini['norm_author'] = self.data_ini[authors_col].apply(
            lambda x: x if pd.isnull(x) else self._normalize_author(x))
        self.data_ini['norm_poem'] = self.data_ini[poems_col].apply(
            lambda x: x if pd.isnull(x) else self._normalize_poem(x))

    def _normalize_author(self, name):
        return name.replace('ё', 'е').lower().strip()

    def _normalize_poem(self, name):
        return re.sub(r'[^а-яА-Яa-zA-Z0-9 ]', '', name).lower().strip()

    def _get_full_texts(self, authors, poems):
        results = []
        norm_authors = [self._normalize_author(a) for a in authors]
        norm_poems = [self._normalize_poem(p) for p in poems]

        res = []
        for a, p in zip(norm_authors, norm_poems):
            all_poem = self.data_ini.loc[
                (self.data_ini.norm_author == a) & (self.data_ini.norm_poem == p),
                self.txt_col
            ].values
            if all_poem.shape[0] > 0:
                res.append(f"{a} '{p}':")
                res.append(all_poem[0])

        return '\n\n'.join(res)

    def _truncate_texts(self, texts):
        chunks = self.splitter.split_text(texts)
        return chunks[0] if chunks else texts

    def prepare_context(self, query, response, rag_method="similarity", k=5):
        print("[DEBUG] prepare_context INN")
        filters = {}
        if response['is_direct'] == 1:
            texts = self._get_full_texts(response['authors'], response['poems'])
            context = self._truncate_texts(texts) if texts else ""
        else:
            rag_query = ', '.join(response['keywords']) if response.get('keywords') else query
            print("[DEBUG] prepare_context ELSE", rag_query)

            if response.get("authors"):
                filters["author"] = {"$in": response["authors"]}
            if response.get("poems"):
                filters["name"] = {"$in": response["poems"]}

            results = self.rag_svc.search(rag_query, method=rag_method, k=k, filters=filters)
            print("[DEBUG] prepare_context results", results)
            if results:
                context = []
                for doc in results:
                    context.append(f"{doc.metadata.get(self.authors_col, '')} '{doc.metadata.get(self.poems_col, '')}':")
                    context.append(doc.page_content)
                context = "\n\n".join(context)
            else:
                context = ""
            print("[DEBUG] prepare_context context", context)

        return context
