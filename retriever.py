#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

from indexer import Indexer
from collections import Counter
import os
import glob
import operator
import math


class Retriever:

    def __init__(self):
        self.query = ''
        self.ind = Indexer()
        return

    def rank_docs_by_query(self, query=''):
        self.query = raw_input("Enter the search query\n") if query == '' else query
        query_terms = self.query.lower().split()
        query_dict = dict(Counter(query_terms))
        m_query = 0
        for each in query_dict:
            m_query += math.pow(query_dict[each], 2)

        mag_query = math.sqrt(m_query)
        inv_index = self.ind.build_n_gram_index(1)
        cosine_sim = {}
        os.chdir('..')
        ind = Indexer()
        doc_dict_id = ind.build_docid_dict(ret=True)
        parsed_corpus = os.path.join(os.getcwd(), 'parsed_corpus')
        os.chdir(parsed_corpus)
        docset = []
        for each in query_terms:
            doclist = inv_index[each]
            for d in doclist:
                docset.append(d)
        docset = list(set(docset))
        for eachfile in glob.glob('*.txt'):
            fname = eachfile[:len(eachfile) - 4]
            if doc_dict_id[fname] not in docset:
                continue
            file_content = open(eachfile)
            content = file_content.read()
            content = content.split()
            word_count = dict(Counter(content))
            sum_num = 0
            m_doc = 0
            for each in word_count:
                idf_comp = 1 + math.log(float(989)/len(inv_index[each]))
                tf_word = word_count[each]/float(len(content))
                m_doc += math.pow(tf_word*idf_comp, 2)
            mag_doc = math.sqrt(m_doc)

            for each_query_term in query_terms:
                if each_query_term in content:
                    tf = word_count[each_query_term]/float(len(content))
                    idf = 1 + math.log(float(989)/len(inv_index[each_query_term]))
                    x = tf*idf
                    sum_num += x*query_terms.count(each_query_term)
                else:
                    continue
            denominator = mag_query*mag_doc
            similarity = sum_num/denominator
            cosine_sim[fname] = similarity
        sorted_cosine_dict = sorted(cosine_sim.items(), key=operator.itemgetter(1), reverse=True)
        sorted_cosine_dict = sorted_cosine_dict[:100]
        return sorted_cosine_dict

    def run_query(self, query, queryid):
        print "running query : " + query
        ranked_docs = self.rank_docs_by_query(query)
        os.chdir('..')
        ind = Indexer()
        doc_dict_id = ind.build_docid_dict(ret=True)
        fname = '%s.txt' % query
        f = open(fname, 'w')
        for each in ranked_docs:
            f.write('{} {} {} {} {} {}\n'.format(queryid, 'Q0',
                                                 doc_dict_id[each[0]],
                                                 # each[0],
                                                 ranked_docs.index(each)+1, each[1], 'system_name'))
        f.close()

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
    queries = dict()
    queries['global warming potential'] = 1
    queries['green power renewable energy'] = 2
    queries['solar energy california'] = 3
    queries['light bulb bulbs alternative alternatives'] = 4
    live = True
    print "Welcome to search\n"
    while live:
        query = raw_input('\n\nEnter the query (type \'exit\' to end and \'hw4\' to run the assignment)\n')
        if query == 'exit':
            break
        elif query == 'hw4':
            for each in queries:
                r.run_query(each, queries[each])
        else:
            query_id = queries[query] if query in queries else 0
            r.run_query(query, query_id)
    # r.modify_lucene_files()
    # r.merge_files('Ranked_Docs')
    return

hw4_tasks()