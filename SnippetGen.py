#! /usr/bin/env python
from FileAccess import FileAccess


class SnippetGenerator:

    def __init__(self):
        self.max = 150
        return



    def generate_snippet(self, doc, query):
        fa = FileAccess()
        stop_words = fa.get_stop_words()
        query = query.split()
        stopped_content = query
        final_query = " ".join(stopped_content)

        fq_list = final_query.split()
        doc_list = doc.split()
        intr = list(set(doc_list).intersection(fq_list))

        positions = []
        for each in intr:
            if each in intr:
                key = doc_list.index(each)
                positions.append(key)
            else:
                continue
        final_doc = ''
        i = 0
        for each in doc_list:
            if i in positions:
                q = '"'+each+'" '
                final_doc += q
            else:
                final_doc += each + ' '
            i += 1

        return final_doc








