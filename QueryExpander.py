#! /usr/bin/env python

# Author : Ashok, Sravanthi and Frenia
# Date   : 6th December 2016
# Task   : IR Final Project


from retriever import Retriever
from collections import Counter
import operator
from FileAccess import FileAccess


class QueryExpander:

    def __init__(self, filename, query_dict, top_k=15, n=25):
        r = Retriever()
        corpus = r.get_total_corpus()
        self.k = top_k
        self.n = n
        self.total_corpus = corpus
        fa = FileAccess()
        self.query_dict = query_dict
        self.results = fa.read_result_file(filename=filename)
        return

    def psuedo_relevance_feedback(self, query_id):
        results = self.results[query_id]
        query = self.query_dict[query_id]
        results = results[0:self.k]
        whole_content = []
        for eachdoc in results:
            whole_content.extend(self.total_corpus[eachdoc])

        word_count = dict(Counter(whole_content))
        query_terms = query.split()

        for eachterm in query_terms:
            if eachterm in word_count:
                word_count[eachterm] += self.k
            else:
                word_count[eachterm] = self.k
        weighted_words = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
        weighted_words = weighted_words[0:len(query_terms) + self.n]
        extra_query = ''
        for each in weighted_words:
            extra_query += each[0]+' '
        final_query = query + ' ' + extra_query
        return final_query

    def get_expanded_queries(self):
        query_dict = self.query_dict
        expanded_queries = {}
        for each in query_dict:
            query_id = each
            exp_query = self.psuedo_relevance_feedback(query_id)
            expanded_queries[query_id] = exp_query

        return expanded_queries

