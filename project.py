#! /usr/bin/env python

from retriever import Retriever
from RetrievalModel import TfIdf, CosineSimilarity, BM25
from FileAccess import FileAccess
from QueryExpander import QueryExpander
from StopAndStem import Stemmer, Stopper
from Evaluation import Evaluation
import os

def task1(notes = ''):
    r = Retriever()
    fa = FileAccess()
    query_dict = fa.read_queries()
    corpus = r.get_corpus(True)
    inverted_index = corpus[0]
    total_corpus = corpus[1]
    relevance_data = fa.get_relevance_data()

    r.run_all_queries(inverted_index=inverted_index,total_corpus=total_corpus,relevance_data=relevance_data,
                     query_dict=query_dict, model="tfidf", task_id="1", notes=notes)

    r.run_all_queries(inverted_index=inverted_index, total_corpus=total_corpus, relevance_data=relevance_data,
                         query_dict=query_dict, model='cosine', task_id="1", notes=notes)

    r.run_all_queries(inverted_index=inverted_index, total_corpus=total_corpus, relevance_data=relevance_data,
                         query_dict=query_dict, model='bm25', task_id="1", notes=notes)



def task2(model):
    fa = FileAccess()
    r = Retriever()
    corpus = r.get_corpus(True)
    inverted_index = corpus[0]
    total_corpus = corpus[1]
    relevance_data = fa.get_relevance_data()
    task1_folder = os.path.join(os.getcwd(), 'task1')
    file_name = "task1_"+model+".txt"
    result_file = task1_folder+'/'+file_name
    qe = QueryExpander(result_file)
    expanded_queries = qe.get_expanded_queries()
    r.run_all_queries(inverted_index=inverted_index, total_corpus=total_corpus, relevance_data=relevance_data,
                      query_dict=expanded_queries, model='cosine', task_id="2", notes="expanded", store_queries='expanded')



def task3a():
    stop = Stopper()
    stop.build_stopped_inverted_index()

def task3b():
    stem = Stemmer()
    stem.build_stemmed_data()
    return

def task4():
    return

def evalaution():
    e = Evaluation()
    # scores = e.read_file('task1_cosine.txt')
    files = ['task1_tfidf.txt',
             "task1_cosine.txt",
             'task1_bm25.txt',
             'task1_lucene.txt']
    for f in files:
        e.evaluate(f)
    return

# task1()
task2('cosine')


