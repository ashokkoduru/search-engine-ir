#! /usr/bin/env python

import glob
import os

class FileAccess:
    def __init__(self):
        return

    def get_relevance_data(self):
        relevance_data = {}
        with open("cacm.rel") as content:
            data = content.read().splitlines()
        data = [s.split() for s in data]
        for qid in data:
            relevance_data.setdefault(int(qid[0]), []).append(qid[2])
        return relevance_data

    def read_queries(self):
        with open("cleaned_queries.txt") as content:
            queries = content.read().splitlines()

        query_dict = {}
        for q in queries:
            each = q.split()
            query_id = int(each[0])
            query = " ".join(each[1:])
            query_dict[query_id] = query

        return query_dict

    def read_result_file(self, filename):
        results = {}
        with open(filename) as f:
            data = f.read().splitlines()
        data = [s.split() for s in data]
        for each in data:
            results.setdefault(int(each[0]), []).append(each[2])
        return results

    def get_stop_words(self):
        print os.getcwd()
        with open('common_words') as f:
            stop_words = f.read().splitlines()

        return stop_words

    def read_score_file(self, file_name):
        with open(file_name) as f:
            data = f.read().splitlines()

        data = [s.split() for s in data]
        scores = {}
        for each in data:
            d = (each[2], each[4])
            scores.setdefault(int(each[0]), []).append(d)
        return scores

    def get_stem_queries(self):
        with open('cacm_stem.query.txt') as f:
            data = f.read().splitlines()

        stemmed_queries = {}
        i = 1
        for each in data:
            stemmed_queries[i] = each
            i += 1

        return stemmed_queries

