#! /usr/bin/env python

from retriever import Retriever
from SnippetGen import SnippetGenerator
from FileAccess import FileAccess
from QueryExpander import QueryExpander
from StopAndStem import Stemmer, Stopper
from Evaluation import Evaluation
import os, glob

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
    file_name = "task1_"+model+"_.txt"
    result_file = task1_folder+'/'+file_name
    qe = QueryExpander(query_dict=query_dict, filename=result_file, clean=True)
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


def phase2(model):
    stop = Stopper()
    stopped_corpus = stop.build_stopped_inverted_index()
    stop_inv_index = stopped_corpus[0]
    stop_total_corpus = stopped_corpus[1]
    task3a_folder = os.path.join(os.getcwd(), 'task3a')
    file_name = "task3a_cosine_stopped.txt"
    r = Retriever()
    fa = FileAccess()
    relevance_data = fa.get_relevance_data()
    query_dict = fa.read_queries()
    result_file = task3a_folder + '/' + file_name
    stopped_queries = stop.get_stopped_queries(query_dict)
    qe = QueryExpander(query_dict=stopped_queries, filename=result_file, clean=False)
    expanded_stopped_queries = qe.get_expanded_queries()
    r.run_all_queries(inverted_index=stop_inv_index, total_corpus=stop_total_corpus, relevance_data=relevance_data,
                      query_dict=expanded_stopped_queries, model=model, task_id="phase2", notes="stopped_expanded", store_queries='stopped_expanded')


def evalaution():
    p_k = [5, 20]
    fa = FileAccess()
    relevance_data = fa.get_relevance_data()
    base_dir = os.getcwd()
    all_runs = os.path.join(os.getcwd(), 'all_runs')
    os.chdir(all_runs)
    e = Evaluation()

    for eachfile in glob.glob('*.txt'):
        e.evaluate(eachfile, p_k, base_dir, relevance_data)


def snippet_generation():
    r = Retriever()
    fa = FileAccess()
    query_dict = fa.read_queries()
    query_id = raw_input('Enter the query_id: \n')
    if int(query_id) > 64 or int(query_id) < 1:
        print 'No Query exists, please enter between 1 to 64'
        return
    query = query_dict[int(query_id)-1]
    print 'Query: '+ query
    fa = FileAccess()
    relevance_data = fa.get_relevance_data()
    corpus = r.get_corpus(True)
    inverted_index = corpus[0]
    total_corpus = corpus[1]

    results = r.run_all_queries(inverted_index=inverted_index, total_corpus=total_corpus, relevance_data=relevance_data,
                                query_dict=query_dict, model='cosine', task_id="1", notes='', ret=True)

    results = results[0:10]
    snippet_dictionary = {}

    for each in results:
        docid = each[1]
        data = total_corpus[docid]
        data = " ".join(data)
        sg = SnippetGenerator()
        snippet = sg.generate_snippet(data, query)
        snippet_dictionary[docid] = snippet

    for each in results:
        print each[1]
        print snippet_dictionary[each[1]]
        print '\n'


# uncomment the particular method that needs to be run

# change this to bm25 or tfidf if required
model = 'cosine'

# Task 1 : It runs the 3 models and creates the folder task1
# task1()

# Task 2 : It runs the cosine model on expanded queries and creates the folder task2
# task2(model)

# Task 3a: It runs the cosine model on stopped queries and stopped corpus
# task3a(model)

# Task 3b: It runs the cosine model on stemmed queries and stemmed corpus
# task3b(model)

# Task phase2: It runs the cosine model on stemmed queries and stemmed corpus
# phase2(model)

# Evaluation : It takes all the runs present in all_runs folder and do the evaluation on them
# evalaution()

# Snippet: prompts a query id and generates relevant snippetes
snippet_generation()



