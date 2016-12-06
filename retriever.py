#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

from indexer import Indexer
from collections import Counter
from bs4 import BeautifulSoup
import os
import glob
import operator
import math
import re


class Retriever:

    def __init__(self):
        index = self.build_inverted_index()
        self.inverted_index = index[0]
        self.total_corpus = index[1]
        self.token_count = index[2]

    def run_query(self, query, queryid):
        print "running query : " + query
        ranked_docs = self.cosine_similarity(query)
        fname = '%s.txt' % query
        os.chdir('..')
        f = open(fname, 'w')
        for each in ranked_docs:
            f.write('{} {} {} {} {} {}\n'.format(queryid, 'Q0',
                                                 each[0],
                                                 ranked_docs.index(each)+1, each[1], 'system_name'))
        f.close()

    def build_inverted_index(self):
        self.navigate_to_docs()
        inverted_index = {}
        corpus_content = {}
        token_count = {}
        for eachfile in glob.glob('*.html'):
            docid = eachfile[:-5]
            content = open(eachfile).read()
            parsed_content = self.parse_document(content)
            content_as_list = parsed_content.split()
            content_as_list = [s.encode("UTF-8") for s in content_as_list]
            corpus_content[docid] = content_as_list
            token_count[docid] = len(content_as_list)
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
        return inverted_index, corpus_content, token_count

    def cosine_similarity(self, query):
        query_terms = query.lower().split()
        query_dict = dict(Counter(query_terms))
        m_query = 0
        for each in query_dict:
            m_query += math.pow(query_dict[each], 2)

        mag_query = math.sqrt(m_query)
        inv_index = self.inverted_index
        total_corpus = self.total_corpus
        cosine_similarity = {}
        docset = []
        for each in query_terms:
            doclist = inv_index[each]
            for d in doclist:
                docset.append(d)
        docset = list(set(docset))
        for eachfile in total_corpus:
            docid = eachfile[:-5]
            if docid not in docset:
                continue
            content = total_corpus[docid]
            word_count = dict(Counter(content))
            sum_num = 0
            m_doc = 0
            for each in word_count:
                idf_comp = 1 + math.log(float(len(total_corpus))/len(inv_index[each]))
                tf_word = word_count[each]/float(len(content))
                m_doc += math.pow(tf_word*idf_comp, 2)
            mag_doc = math.sqrt(m_doc)

            for each_query_term in query_terms:
                if each_query_term in content:
                    tf = word_count[each_query_term]/float(len(content))
                    idf = 1 + math.log(float(len(total_corpus))/len(inv_index[each_query_term]))
                    x = tf*idf
                    sum_num += x*query_terms.count(each_query_term)*1
                else:
                    continue
            denominator = mag_query*mag_doc
            similarity = sum_num/denominator
            cosine_similarity[docid] = similarity
        # sorted_cosine_dict = sorted(cosine_sim.items(), key=operator.itemgetter(1), reverse=True)
        # sorted_cosine_dict = sorted_cosine_dict[:100]
        return cosine_similarity



    def tf_idf(self, query):
        query_terms = query.split()
        corpus_content = self.total_corpus
        tf_idf_scores = {}
        total_files = len(corpus_content)
        for eachfile in corpus_content:
            docid = eachfile[:-5]
            tf_idf_file = 0
            for each_query_term in query_terms:
                tf_term = corpus_content[eachfile].count(each_query_term)
                idf_term = 1 + math.log(float(total_files)/len(self.inverted_index[eachfile]))
                tf_idf_file += tf_term * idf_term
            tf_idf_scores[docid] = tf_idf_file

        return tf_idf_scores

    def navigate_to_docs(self):
        cwd = os.getcwd()
        cacm = os.path.join(cwd, 'cacm')
        os.chdir(cacm)

    def read_queries(self):
        with open("cacm.query") as content:
            regex = re.compile(r'<DOCNO>\s+(.*?)\s+</DOCNO>(.*?)</DOC>', re.DOTALL)
            queries = re.findall(regex, content.read().replace("\n", ''))

        query_file = open('cacm_query.query', 'w')
        for query in queries:
            query_file.write('{} {}\n'.format(query[0], query[1][1:-1]))

    def parse_document(self, file_content):
        content = BeautifulSoup(file_content, 'html.parser')
        content = content.get_text()
        return content


    def modify_lucene_files(self):
        ind = Indexer()
        doc_dict_id = ind.build_docid_dict(ret=True)
        cwd = os.getcwd()
        lucene_files = os.path.join(cwd, 'Lucene Files')
        lucene_deliverables = os.path.join(cwd, 'Lucene_Deliverables')
        if not os.path.exists(lucene_deliverables):
            os.makedirs(lucene_deliverables, 0755)
        os.chdir(lucene_files)
        for eachfile in glob.glob('*.txt'):
            new_list = []
            with open(eachfile) as f:
                listl = f.read().splitlines()
            for line in listl:
                line = line.split()
                line[2] = str(doc_dict_id[line[2]])
                nline = " ".join(line)
                new_list.append(nline)
            fnewname = eachfile[:-4]+'_lucene.txt'
            f = open(os.path.join(lucene_deliverables, fnewname), 'w')
            for line in new_list:
                f.write(line + '\n')
            f.close()
        return

    def merge_files(self, foldername):
        file_list = []
        ranked_docs = os.path.join(os.getcwd(), foldername)
        os.chdir(ranked_docs)
        mergedfile = 'Merged_results_queries.txt1'
        for eachfile in glob.glob('*.txt'):
            file_list.append(eachfile)
        if os.path.exists(mergedfile):
            os.remove(mergedfile)
        with open(mergedfile, 'w') as outfile:
            for fname in file_list:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)


def hw4_tasks():

    r = Retriever()
    # print r.inverted_index['the']
    print r.total_corpus['CACM-0001']
    # r.read_queries()
    # r.build_inverted_index()


    # r.run_query(query, query_id)
    # r.modify_lucene_files()
    # r.merge_files('Ranked_Docs')
    return

hw4_tasks()