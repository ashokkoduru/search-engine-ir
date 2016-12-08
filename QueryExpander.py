#! /usr/bin/env python

# Author : Ashok, Sravanthi and Frenia
# Date   : 6th December 2016
# Task   : IR Final Project
from retriever import Retriever
from collections import Counter
import os
import string
import glob
import operator
import math


class QueryExpander:

    def __init__(self, filename, top_k=15, n=25):
        self.k = top_k
        self.n = n
        r = Retriever()
        corpus = r.get_total_corpus()
        self.total_corpus = corpus
        self.query_dict = r.read_queries()
        self.results = self.read_result_file(filename=filename)
        return

    def read_result_file(self, filename):
        results = {}
        with open(filename) as f:
            data = f.read().splitlines()
        data = [s.split() for s in data]
        for each in data:
            results.setdefault(int(each[0]), []).append(each[2])
        return results

    def psuedo_relevance_feedback(self, query_id):
        results = self.results[query_id]
        query = self.query_dict[query_id]
        # inv_index = corpus[0]
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
            extra_query += each[0]

        return query+extra_query

