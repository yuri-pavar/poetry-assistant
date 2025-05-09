import json
import re
import pandas as pd
import torch
# from app.core.generate_vllm import async_generate
from app.core.generate_vllm import generate_sync
# from app.core.config import SYSTEM_PROMPT


# class Preprocessor:
#     # def __init__(self, model, tokenizer, data, authors_col, poems_col):
#     def __init__(self, data, authors_col, poems_col):
#         # self.tokenizer = tokenizer
#         # self.model = model
#         self.data_ini = data.copy()
#         self.authors_col = authors_col
#         self.poems_col = poems_col

#         self.data_ini['norm_author'] = self.data_ini[self.authors_col].apply(
#             lambda x: x if pd.isnull(x) else self.normalize_author(x))
#         self.data_ini['norm_poem'] = self.data_ini[self.poems_col].apply(
#             lambda x: x if pd.isnull(x) else self.normalize_poem(x))

#     def _structout_json_parser_ner(self, txt):
#         txt_clean = txt.replace("`", "").replace("json", "").strip()
#         try:
#             res_dct = json.loads(txt_clean)
#             authors = res_dct.get('authors', [])
#             poems = res_dct.get('poems', [])
#         except json.JSONDecodeError:
#             authors = []
#             poems = []
#         return authors, poems

#     def _structout_json_parser_rewrite(self, txt):
#         txt_clean = txt.replace("`", "").replace("json", "").strip()
#         try:
#             res_dct = json.loads(txt_clean)
#             keywords = res_dct.get('keywords', [])
#         except json.JSONDecodeError:
#             keywords = []
#         return keywords

#     def normalize_author(self, name):
#         return name.replace('ё', 'е').lower().strip()

#     def normalize_poem(self, name):
#         return re.sub(r'[^а-яА-Яa-zA-Z0-9 ]', '', name).lower().strip()

#     def _check_data_contains(self, author=None, poem=None):
#         if author:
#             author_norm = self.normalize_author(author)
#         if poem:
#             poem_norm = self.normalize_poem(poem)

#         if author and poem:
#             match_df = self.data_ini.loc[(self.data_ini.norm_author == author_norm) & (self.data_ini.norm_poem == poem_norm)]
#         elif author and not poem:
#             match_df = self.data_ini.loc[(self.data_ini.norm_author == author_norm)]
#         else:
#             match_df = self.data_ini.loc[(self.data_ini.norm_poem == poem_norm)]

#         return match_df.shape[0] > 0

#     def _rag_router(self, authors, poems):
#         res_dct = {}

#         if not authors and not poems:
#             res_dct['is_direct'] = 0
#             return res_dct

#         if authors and not poems:
#             res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
#             res_dct['is_direct'] = 0
#         elif not authors and poems:
#             res_dct['poems'] = [poem for poem in poems if self._check_data_contains(poem=poem)]
#             res_dct['is_direct'] = 0
#         elif len(authors) > len(poems):
#             res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
#             res_dct['is_direct'] = 0
#         elif len(authors) == 1 and poems:
#             poems_checked = [poem for poem in poems if self._check_data_contains(author=authors[0], poem=poem)]
#             if poems_checked:
#                 res_dct['poems'] = poems_checked
#                 res_dct['authors'] = [authors[0]] * len(poems_checked)
#                 res_dct['is_direct'] = 1
#             else:
#                 res_dct['authors'] = [authors[0]]
#                 res_dct['is_direct'] = 0
#         elif len(poems) > len(authors):
#             res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
#             res_dct['is_direct'] = 0
#         else:
#             ap_checked = [(a, p) for a, p in zip(authors, poems) if self._check_data_contains(author=a, poem=p)]
#             res_dct['authors'] = [a for a, _ in ap_checked]
#             res_dct['poems'] = [p for _, p in ap_checked]
#             res_dct['is_direct'] = 1

#         return res_dct

#     def process_response_ner(self, response):
#         splitted = response.split('assistant')
#         if len(splitted) > 1:
#             splitted = splitted[1]
#         else:
#             splitted = splitted[-1]

#         authors, poems = self._structout_json_parser_ner(splitted)

#         if len(poems)/max(len(authors), 1) > 2:
#             poems = []

#         return self._rag_router(authors, poems)

#     def process_response_rewrite(self, response):
#         splitted = response.split('assistant')
#         if len(splitted) > 1:
#             splitted = splitted[1]
#         else:
#             splitted = splitted[-1]

#         return self._structout_json_parser_rewrite(splitted)

#     # def generate(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#     #     uprompt = user_prompt.format(query=query)
#     #     messages = [
#     #         {"role": "system", "content": system_prompt},
#     #         {"role": "user", "content": uprompt}
#     #     ]
#     #     input_ids = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to(self.model.device)

#     #     with torch.no_grad():
#     #         output = self.model.generate(
#     #             input_ids,
#     #             max_new_tokens=max_new_tokens,
#     #             do_sample=True,
#     #             temperature=temperature,
#     #             top_p=top_p,
#     #             pad_token_id=self.tokenizer.eos_token_id
#     #         )
#     #     return self.tokenizer.decode(output[0], skip_special_tokens=True)

#     # def generate(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#     #     uprompt = user_prompt.format(query=query)
#     #     return generate_sync(
#     #         prompt=uprompt,
#     #         system_prompt=system_prompt,
#     #         max_tokens=max_new_tokens,
#     #         temperature=temperature,
#     #         top_p=top_p
#     #     )

#     # def get_query_ner(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#     #     return self.process_response_ner(self.generate(query, system_prompt, user_prompt, max_new_tokens, temperature, top_p))
#     # async def get_query_ner(self, query, system_prompt, user_prompt):
#     #     generated = await self.generate_vllm(query, system_prompt, user_prompt)
#     #     return self.process_response_ner(generated)
#     def get_query_ner(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#         uprompt = user_prompt.format(query=query)
#         generated = generate_sync(
#             prompt=uprompt,
#             system_prompt=system_prompt,
#             max_tokens=max_new_tokens,
#             temperature=temperature,
#             top_p=top_p
#         )
#         return self.process_response_ner(generated)


#     # def get_query_rewrite(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#     #     return self.process_response_rewrite(self.generate(query, system_prompt, user_prompt, max_new_tokens, temperature, top_p))
#     # async def get_query_rewrite(self, query, system_prompt, user_prompt):
#     #     generated = await self.generate_vllm(query, system_prompt, user_prompt)
#     #     return self.process_response_rewrite(generated)
#     def get_query_rewrite(self, query, system_prompt, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
#         uprompt = user_prompt.format(query=query)
#         generated = generate_sync(
#             prompt=uprompt,
#             system_prompt=system_prompt,
#             max_tokens=max_new_tokens,
#             temperature=temperature,
#             top_p=top_p
#         )
#         return self.process_response_rewrite(generated)


class Preprocessor:
    def __init__(self, data, authors_col, poems_col):
        self.data_ini = data.copy()
        self.authors_col = authors_col
        self.poems_col = poems_col

        self.data_ini['norm_author'] = self.data_ini[self.authors_col].apply(
            lambda x: x if pd.isnull(x) else self.normalize_author(x))
        self.data_ini['norm_poem'] = self.data_ini[self.poems_col].apply(
            lambda x: x if pd.isnull(x) else self.normalize_poem(x))

    def _structout_json_parser_ner(self, txt):
        txt_clean = txt.replace("`", "").replace("json", "").strip()
        try:
            res_dct = json.loads(txt_clean)
            authors = res_dct.get('authors', [])
            poems = res_dct.get('poems', [])
        except json.JSONDecodeError:
            authors = []
            poems = []
        return authors, poems

    def _structout_json_parser_rewrite(self, txt):
        txt_clean = txt.replace("`", "").replace("json", "").strip()
        try:
            res_dct = json.loads(txt_clean)
            keywords = res_dct.get('keywords', [])
        except json.JSONDecodeError:
            keywords = []
        return keywords

    def normalize_author(self, name):
        return name.replace('ё', 'е').lower().strip()

    def normalize_poem(self, name):
        return re.sub(r'[^а-яА-Яa-zA-Z0-9 ]', '', name).lower().strip()

    def _check_data_contains(self, author=None, poem=None):
        if author:
            author_norm = self.normalize_author(author)
        if poem:
            poem_norm = self.normalize_poem(poem)

        if author and poem:
            match_df = self.data_ini.loc[(self.data_ini.norm_author == author_norm) & (self.data_ini.norm_poem == poem_norm)]
        elif author and not poem:
            match_df = self.data_ini.loc[(self.data_ini.norm_author == author_norm)]
        else:
            match_df = self.data_ini.loc[(self.data_ini.norm_poem == poem_norm)]

        return match_df.shape[0] > 0

    def _rag_router(self, authors, poems):
        res_dct = {}

        if not authors and not poems:
            res_dct['is_direct'] = 0
            return res_dct

        if authors and not poems:
            res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
            res_dct['is_direct'] = 0
        elif not authors and poems:
            res_dct['poems'] = [poem for poem in poems if self._check_data_contains(poem=poem)]
            res_dct['is_direct'] = 0
        elif len(authors) > len(poems):
            res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
            res_dct['is_direct'] = 0
        elif len(authors) == 1 and poems:
            poems_checked = [poem for poem in poems if self._check_data_contains(author=authors[0], poem=poem)]
            if poems_checked:
                res_dct['poems'] = poems_checked
                res_dct['authors'] = [authors[0]] * len(poems_checked)
                res_dct['is_direct'] = 1
            else:
                res_dct['authors'] = [authors[0]]
                res_dct['is_direct'] = 0
        elif len(poems) > len(authors):
            res_dct['authors'] = [author for author in authors if self._check_data_contains(author=author)]
            res_dct['is_direct'] = 0
        else:
            ap_checked = [(a, p) for a, p in zip(authors, poems) if self._check_data_contains(author=a, poem=p)]
            res_dct['authors'] = [a for a, _ in ap_checked]
            res_dct['poems'] = [p for _, p in ap_checked]
            res_dct['is_direct'] = 1

        return res_dct

    def process_response_ner(self, response):
        splitted = response.split('assistant')
        if len(splitted) > 1:
            splitted = splitted[1]
        else:
            splitted = splitted[-1]

        authors, poems = self._structout_json_parser_ner(splitted)

        if len(poems)/max(len(authors), 1) > 2:
            poems = []

        return self._rag_router(authors, poems)

    def process_response_rewrite(self, response):
        splitted = response.split('assistant')
        if len(splitted) > 1:
            splitted = splitted[1]
        else:
            splitted = splitted[-1]

        return self._structout_json_parser_rewrite(splitted)

    # async def get_query_ner(self, query, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
    #     uprompt = user_prompt.format(query=query)
    #     generated = await async_generate(
    #         prompt=uprompt,
    #         # system_prompt=SYSTEM_PROMPT,
    #         max_tokens=max_new_tokens,
    #         temperature=temperature,
    #         # top_p=top_p
    #     )
    #     print(generated)
    #     return self.process_response_ner(generated)

    # async def get_query_rewrite(self, query, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
    #     uprompt = user_prompt.format(query=query)
    #     generated = await async_generate(
    #         prompt=uprompt,
    #         # system_prompt=SYSTEM_PROMPT,
    #         max_tokens=max_new_tokens,
    #         temperature=temperature,
    #         # top_p=top_p
    #     )
    #     return self.process_response_rewrite(generated)


    def get_query_ner(self, query, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
        uprompt = user_prompt.format(query=query)
        generated = generate_sync(
            prompt=uprompt,
            # system_prompt=SYSTEM_PROMPT,
            max_tokens=max_new_tokens,
            temperature=temperature,
            # top_p=top_p
        )
        print(generated)
        return self.process_response_ner(generated)

    def get_query_rewrite(self, query, user_prompt, max_new_tokens=250, temperature=0.7, top_p=0.9):
        uprompt = user_prompt.format(query=query)
        generated = generate_sync(
            prompt=uprompt,
            # system_prompt=SYSTEM_PROMPT,
            max_tokens=max_new_tokens,
            temperature=temperature,
            # top_p=top_p
        )
        return self.process_response_rewrite(generated)