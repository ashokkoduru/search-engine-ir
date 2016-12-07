#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

from indexer import Indexer
from collections import Counter
from bs4 import BeautifulSoup
from RetrievalModel import TfIdf, CosineSimilarity, BM25
import os
import glob
import operator
import math
import re


class Retriever:

    def __init__(self):
        index = self.build_index()
        self.inverted_index = index[0]
        self.total_corpus = index[1]
        self.relevance_data = self.get_relevance_data()

    def clean_corpus(self):
        cwd = os.getcwd()
        cacm = os.path.join(cwd, 'cacm')
        clean_cacm = os.path.join(cwd, 'clean_cacm')

        if not os.path.exists(cacm):
            print "Corpus doesn't exist. It is created now. " \
                  "PLease put raw files inside the corpus folder"
            os.makedirs(cacm, 0755)
            return
        if not os.path.exists(clean_cacm):
            os.makedirs(clean_cacm, 0755)

        os.chdir(cacm)

        for eachfile in glob.glob('*.html'):
            content = open(eachfile).read()
            content = BeautifulSoup(content, 'html.parser')
            content = content.get_text().encode('utf-8')
            clean_content = self.clean_content(content, True)
            clean_file = open(os.path.join(clean_cacm, eachfile), 'w')
            clean_file.write(clean_content)
            clean_file.close()

    def clean_content(self, content, not_query):
        ignore_list = ['!', '@', '#', '$', '^', '&', '*', '(', ')', '_', '+', '=', '{', '[', '}', ']', '|',
                       '\\', '"', "'", ';', '/', '<', '>', '?', '%']
        content = content.translate(None, ''.join(ignore_list))
        content = content.split()
        last = 0
        if not_query:
            for i, v in enumerate(reversed(content)):
                if v == 'AM' or v == 'PM':
                    last = len(content) - i - 1
                    break
            content = content[0:last+1]
        final_content = ''
        for eachword in content:
            if len(eachword) > 1 and eachword[0] == '-':
                eachword = eachword[1:]
            eachword = eachword.lower()
            eachword = eachword.strip('.,-')
            if eachword == '-':
                continue
            final_content += eachword + ' '
        return final_content

    def build_index(self):
        cwd = os.getcwd()
        clean_cacm = os.path.join(cwd, 'clean_cacm')
        os.chdir(clean_cacm)
        inverted_index = {}
        total_corpus = {}
        for eachfile in glob.glob('*.html'):
            docid = eachfile[:-5]
            content = open(eachfile).read()
            content_as_list = content.split()
            total_corpus[docid] = content_as_list
            word_count = dict(Counter(content_as_list))
            for token in content_as_list:
                if token not in inverted_index:
                    temp = dict()
                    temp[docid] = word_count[token]
                    inverted_index[token] = temp
                else:
                    temp = inverted_index[token]
                    temp[docid] = word_count[token]
                    inverted_index[token] = temp
        os.chdir('..')
        return inverted_index, total_corpus

    def get_relevance_data(self):
        relevance_data = {}
        with open("cacm.rel") as content:
            data = content.read().splitlines()
        data = [s.split() for s in data]
        for qid in data:
            relevance_data.setdefault(int(qid[0]), []).append(qid[2])
        return relevance_data

    def read_queries(self):
        with open("cacm.query") as content:
            regex = re.compile(r'<DOCNO>\s+(.*?)\s+</DOCNO>(.*?)</DOC>', re.DOTALL)
            queries = re.findall(regex, content.read().replace("\n", ' '))

        query_file = open('cacm_query.query', 'w')
        for query in queries:
            query_file.write('{} {}\n'.format(query[0], query[1][1:-1]))


    def run_all_queries(self):
        with open('cacm_query.query') as f:
            queries = f.read().splitlines()

        queries = [s.split() for s in queries]
        query_dict = {}
        for q in queries:
            query_dict[int(q[0])] = " ".join(q[1:])
        results = []
        bm = BM25(self.inverted_index, self.total_corpus, self.relevance_data)
        tfidf = TfIdf(self.inverted_index, self.total_corpus)
        cosine = CosineSimilarity(self.inverted_index, self.total_corpus)
        for each_query in query_dict:
            query = self.clean_content(query_dict[each_query], False)
            # ranks = tfidf.get_tf_idf(query)
            ranks = bm.calculate_bm25(query,each_query)
            # ranks = cosine.get_cosine_similarity(query)
            sorted_results = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)
            sorted_results = sorted_results[:100]
            for each in sorted_results:
                tup = (each_query, each[0], each[1])
                results.append(tup)

        f = open('dummy_bm25.txt', 'w')
        for each in results:
            f.write("{} {} {}\n".format(each[0], each[1], each[2]))

        f.close()


def hw4_tasks():
    r = Retriever()
    # r.clean_corpus()
    # print r.inverted_index['the']
    # print r.total_corpus['CACM-0001']
    # r.read_queries()
    r.run_all_queries()
    # r.get_relevance_data()
    # r.build_inverted_index()
    # r.run_query(query, query_id)
    # r.modify_lucene_files()
    # r.merge_files('Ranked_Docs')
    return

hw4_tasks()