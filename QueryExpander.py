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
        return results

    def psuedo_relevance(self, query_id):
        query_terms={}
        new_query_terms=[]
        docs = self.results[query_id]
        docs = docs[:self.k]
        for eachdoc in docs:
            content = self.total_corpus[eachdoc]
            word_count = dict(Counter(content))
            for token in content:
                if token not in query_terms:
                    query_terms[token] = 1
                else:
                    query_terms[token] += 1
            sorted_wc = sorted(query_terms.items(), key=operator.itemgetter(1), reverse=True)
        for key in sorted_wc[:10]:
            new_query_terms.append(key[0])


        return new_query_terms

    def retrieve_top_k(self):

        with open('cleaned_queries.txt') as f:
            queries = f.read().splitlines()
        queries = [s.split() for s in queries]
        query_dict = {}
        for q in queries:
            query_dict[int(q[0])] = " ".join(q[1:])
        print query_dict
        for key in query_dict:
            new_query_terms = self.psuedo_relevance(key)
            terms = query_dict[key].split()
            final_query=new_query_terms + terms
            final_query = list(set(final_query))
            print(final_query)






def hw3_tasks():
    r = Retriever(need_index= False)

    qe = QueryExpander(inverted_index=r.inverted_index, total_corpus=r.total_corpus)
    #qe.read_result_file('dummy_bm25.txt')
    #qe.psuedo_relevance(1)
    qe.retrieve_top_k()
    # This method builds the clean corpus from raw corpus
    # ind.build_parsed_corpus()
    # print ind.parse_page(s)
    # ind.save_docids()
    return

hw3_tasks()
