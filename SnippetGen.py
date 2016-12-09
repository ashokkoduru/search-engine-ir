#! /usr/bin/env python

from stemming.porter2 import stem
import string


class SnippetGenerator:

    def __init__(self):
        return

    def split_doc_to_tokens(self, doc):
        token_list = []
        exclude = set(string.punctuation)
        doc = doc.split(' ')

        for i in range(len(doc)):
            token = dict()
            token['original'] = doc[i]
            token['stemmed'] = stem(''.join(ch for ch in doc[i] if ch not in exclude).lower())
            token['stemmed'] = stem(doc[i])
            token['op'] = len(' '.join(doc[:i + 1])) - len(doc[i])
            token_list.append(token)

        return token_list

    def build_doc_from_tokens(self, token_list, stemmed=True):
        result = ''
        if stemmed:
            for i in range(len(token_list)):
                result = ' '.join([result, token_list[i]['stemmed']])
            return result.strip()
        else:
            for i in range(len(token_list)):
                result = ' '.join([result, token_list[i]['original']])
            return result.strip()

    def add_from_surround(self, doc_tokens, query_tokens):
        doc = self.build_doc_from_tokens(doc_tokens, False)
        if len(doc) < 200:
            return [doc]
        surround_tokens = []
        keyword_sp = []
        query_token = query_tokens[0]
        for query_token in query_tokens:
            for doc_token in doc_tokens:
                if query_token['stemmed'] == doc_token['stemmed']:
                    keyword_sp.append((doc_token['op'], doc_token['original']))

        if keyword_sp == []:
            return [doc[200:]]

        for i in range(len(keyword_sp)):
            surround_tokens.append(self.extract_surround(doc, keyword_sp[i][0], True, True))
            surround_tokens.append(self.extract_surround(doc, keyword_sp[i][0] + 200 / 2, False, True))
            surround_tokens.append(self.extract_surround(doc, keyword_sp[i][0] + len(keyword_sp[i][1]) - 200 / 2,
                                                         True, False))

        return surround_tokens

    def extract_surround(self, doc, index, flag_left, flag_right):
        left = max(index - 200 / 2, 0)
        right = min(index + 200 / 2, len(doc))
        if right == len(doc):
            flag_right = False
        if left == 0:
            flag_left = False

        left_pf = False
        if flag_left and doc[left - 1].isalnum() and doc[left].isalnum():
            i = left
            while doc[i] != ' ':
                i += 1
            if i - left >= 4:
                left_pf = True
            left = i

        right_pf = False
        if flag_right and doc[right].isalnum() and doc[right - 1].isalnum():
            j = right
            while doc[j] != ' ':
                j -= 1
            if right - j >= 4:
                right_pf = True
            right = j

        surround = (doc[left:right]).strip()
        if left_pf:
            surround = "".join(['... ', surround])
        if right_pf:
            surround = "".join([surround, ' ...'])
        return surround

    def calculate_snippet_score(self, surrounds, doc_tokens, query_tokens):
        max_score = -1
        for surround in surrounds:
            surround_token_list = self.split_doc_to_tokens(surround)
            score = 0
            for query_token in query_tokens:
                for surround_token in surround_token_list:
                    if query_token['stemmed'] == surround_token['stemmed']:
                        doc_count = 0
                        for doc_token in doc_tokens:
                            if doc_token['stemmed'] == query_token['stemmed']:
                                doc_count += 1

                        score += 1. / doc_count

            if score > max_score:
                max_score = score
                best_surround_tokens = surround_token_list

        return best_surround_tokens

    def put_quotes(self, best_surround_tokens, query_tokens):
        snippet = ''
        query_tokenized = self.build_doc_from_tokens(query_tokens)
        for surround_token in best_surround_tokens:
            if surround_token['stemmed'] in query_tokenized.split():

                snippet = ' '.join([snippet, '"'])
                snippet = ''.join([snippet, surround_token['original']])
                snippet = ''.join([snippet, '"'])
            else:
                snippet = ' '.join([snippet, surround_token['original']])
        return snippet.replace('" "', ' ').strip()

    def generate_snippet(self, doc, query):
        sg = SnippetGenerator()
        doc_tokens = self.split_doc_to_tokens(doc.lower())
        query_tokens = self.split_doc_to_tokens(query)
        fragments = self.add_from_surround(doc_tokens, query_tokens)
        best_surround_tokens = self.calculate_snippet_score(fragments, doc_tokens, query_tokens)
        return sg.put_quotes(best_surround_tokens, query_tokens)


def dummy():
    sg = SnippetGenerator()
    doc = ''
    query = ''
    doc_tokens = sg.split_doc_to_tokens(doc)
    query_tokens = sg.split_doc_to_tokens(query)
    fragments = sg.add_from_surround(doc_tokens, query_tokens)
    list_of_best_fragment_tokens = sg.calculate_snippet_score(fragments, doc_tokens, query_tokens)

    # 4. We format the most relevant fragment and return it
    print sg.put_quotes(list_of_best_fragment_tokens, query_tokens)

dummy()


