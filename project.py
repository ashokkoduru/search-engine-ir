#! /usr/bin/env python

from retriever import Retriever
from RetrievalModel import TfIdf, CosineSimilarity, BM25
from FileAccess import FileAccess
from QueryExpander import QueryExpander
from StopAndStem import Stemmer, Stopper
from Evaluation import Evaluation
import os

models = ['tfidf', 'cosine', 'bm25']


def task1(notes=''):
    r = Retriever()
    fa = FileAccess()
    query_dict = fa.read_queries()
    corpus = r.get_corpus(True)
    inverted_index = corpus[0]
    total_corpus = corpus[1]
    relevance_data = fa.get_relevance_data()

    for model in models:
        r.run_all_queries(inverted_index=inverted_index,total_corpus=total_corpus,relevance_data=relevance_data,
                         query_dict=query_dict, model=model, task_id="1", notes=notes)



def task2(model):
    fa = FileAccess()
    r = Retriever()
    query_dict = fa.read_queries()
    corpus = r.get_corpus(True)
    inverted_index = corpus[0]
    total_corpus = corpus[1]
    relevance_data = fa.get_relevance_data()
    task1_folder = os.path.join(os.getcwd(), 'task1')
    file_name = "task1_"+model+".txt"
    result_file = task1_folder+'/'+file_name
    qe = QueryExpander(query_dict=query_dict, filename=result_file)
    expanded_queries = qe.get_expanded_queries()
    r.run_all_queries(inverted_index=inverted_index, total_corpus=total_corpus, relevance_data=relevance_data,
                      query_dict=expanded_queries, model='cosine', task_id="2", notes="expanded", store_queries='expanded')



def task3a(model):
    stop = Stopper()
    stopped_corpus = stop.build_stopped_inverted_index()
    stop_inv_index = stopped_corpus[0]
    stop_total_corpus = stopped_corpus[1]
    fa = FileAccess()
    r = Retriever()
    query_dict = fa.read_queries()
    relevance_data = fa.get_relevance_data()
    stopped_queries = stop.get_stopped_queries(query_dict)
    r.run_all_queries(inverted_index=stop_inv_index, total_corpus=stop_total_corpus, relevance_data=relevance_data,
                      query_dict=stopped_queries, model=model, task_id="3a", notes="stopped", store_queries='stopped')


def task3b(model):
    stem = Stemmer()
    r = Retriever()
    stem_total_corpus = stem.build_stemmed_data()
    stem_inv_index = stem.build_stemmed_index()
    fa = FileAccess()
    relevance_data = fa.get_relevance_data()
    stemmed_queries = fa.get_stem_queries()

    r.run_all_queries(inverted_index=stem_inv_index, total_corpus=stem_total_corpus, relevance_data=relevance_data,
                      query_dict=stemmed_queries, model=model, task_id="3b", notes="stemmed", store_queries='stemmed')


def pahse2():

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
# task2('cosine')
# task3a('cosine')
task3b('cosine')


