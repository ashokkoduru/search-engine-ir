from retriever import Retriever
from RetrievalModel import TfIdf, CosineSimilarity, BM25
from QueryExpander import QueryExpander
from StopAndStem import Stemmer, Stopper
from Evaluation import Evaluation

def task1():
    r = Retriever()
    r.run_task1()
    return

def task2():
    qe = QueryExpander('task1_lucene.txt')
    query = qe.psuedo_relevance_feedback(1)
    print query
    return

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


