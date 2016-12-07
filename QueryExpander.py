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

    def __init__(self, inverted_index={}, total_corpus={}, filename='dummy_bm25.txt', top_k=15, n=10):
        self.inverted_index = inverted_index
        self.total_corpus = total_corpus
        self.results = self.read_result_file(filename)
        self.k = top_k
        return

    def read_result_file(self, filename):
        results = {}
        with open(filename) as f:
            data = f.read().splitlines()
        data = [s.split() for s in data]
        for qid in data:
            results.setdefault(int(qid[0]), []).append(qid[1])
        print results

    def psuedo_relevance(self, query_id):
        docs = self.results[query_id]
        docs = docs[:self.k]
        for eachdoc in docs:
            content = self.total_corpus[eachdoc]
            word_count = dict(Counter(content))
            sorted_wc = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)

        return

    def retrieve_top_k(self):

        return





def hw3_tasks():
    r = Retriever(need_index= False)

    qe = QueryExpander(inverted_index=r.inverted_index, total_corpus=r.total_corpus)
    qe.read_result_file('dummy_bm25.txt')
    # This method builds the clean corpus from raw corpus
    # ind.build_parsed_corpus()
    # print ind.parse_page(s)
    # ind.save_docids()
    return

hw3_tasks()
