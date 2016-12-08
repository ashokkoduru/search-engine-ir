#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

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
        return

    def get_corpus(self, req):
        corpus = self.build_index(req)
        return corpus

    def get_total_corpus(self, folder='clean'):
        cwd = os.getcwd()
        if folder == 'clean':
            fol = os.path.join(cwd, 'clean_cacm')
        else:
            fol = os.path.join(cwd, 'stopped_cacm')
        os.chdir(fol)
        total_corpus = {}
        for eachfile in glob.glob('*.html'):
            print eachfile
            docid = eachfile[:-5]
            content = open(eachfile).read()
            content_as_list = content.split()
            total_corpus[docid] = content_as_list
        os.chdir('..')
        return total_corpus

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
        content = content.replace(':', ' ')
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

    def build_index(self,need_index=True, folder='clean'):
        cwd = os.getcwd()
        if folder == 'clean':
            fol = os.path.join(cwd, 'clean_cacm')
        else:
            fol = os.path.join(cwd, 'stopped_cacm')
        os.chdir(fol)
        inverted_index = {}
        total_corpus = {}
        for eachfile in glob.glob('*.html'):
            docid = eachfile[:-5]
            content = open(eachfile).read()
            content_as_list = content.split()
            total_corpus[docid] = content_as_list
            if not need_index:
                continue
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
        with open("cleaned_queries.txt") as content:
            queries = content.read().splitlines()

        query_dict = {}
        for q in queries:
            each = q.split()
            query_id = int(each[0])
            query = " ".join(each[1:])
            query_dict[query_id] = query

        return query_dict

    def run_task1(self, notes = ''):
        query_dict = self.read_queries()
        corpus = self.get_corpus(True)
        inverted_index = corpus[0]
        total_corpus = corpus[1]

        relevance_data = self.get_relevance_data()

        self.run_all_queries(inverted_index=inverted_index,
                             total_corpus=total_corpus,
                             relevance_data=relevance_data,
                             query_dict=query_dict,
                             model="tfidf",
                             task_id="1", notes=notes)

        self.run_all_queries(inverted_index=inverted_index,
                             total_corpus=total_corpus,
                             relevance_data=relevance_data,
                             query_dict=query_dict,
                             model='cosine',
                             task_id="1", notes=notes)

        self.run_all_queries(inverted_index=inverted_index,
                             total_corpus=total_corpus,
                             relevance_data=relevance_data,
                             query_dict=query_dict,
                             model='bm25',
                             task_id="1", notes=notes)

    def run_all_queries(self, inverted_index, total_corpus, relevance_data,
                        query_dict, model='bm25', task_id='', notes=''):
        results = []

        bm = BM25(inverted_index, total_corpus, relevance_data)
        tf_idf = TfIdf(inverted_index, total_corpus)
        cosine = CosineSimilarity(inverted_index, total_corpus)
        for query_id in query_dict:
            query = self.clean_content(query_dict[query_id], False)
            if model == 'tfidf':
                ranks = tf_idf.get_tf_idf(query)
            elif model == 'cosine':
                ranks = cosine.get_cosine_similarity(query)
            else:
                ranks = bm.calculate_bm25(query, query_id)

            sorted_results = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)
            sorted_results = sorted_results[:100]
            rank = 1
            for each in sorted_results:
                tup = (query_id, each[0], rank, each[1], model)
                results.append(tup)
                rank += 1

        result_file_name = 'task'+task_id+'_'+model+notes+'.txt'

        f = open(result_file_name, 'w')
        for each in results:
            f.write('{} {} {} {} {} {}\n'.format(each[0], 'Q0', each[1], each[2], each[3], model))
        f.close()