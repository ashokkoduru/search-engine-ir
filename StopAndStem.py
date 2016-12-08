#! /usr/bin/env python

import os
import glob
from retriever import Retriever
from collections import Counter
# from RetrievalModel import BM25

class Stopper:

    def __init__(self):
        return

    def build_stopped_corpus(self):
        cwd = os.getcwd()
        clean_cacm = os.path.join(cwd, 'clean_cacm')
        stopped_cacm = os.path.join(cwd, 'stopped_cacm')

        if not os.path.exists(clean_cacm):
            print "Clean corpus doesn't exist. It is created now. " \
                  "PLease put cleaned files inside the corpus folder"
            os.makedirs(clean_cacm, 0755)
            return
        if not os.path.exists(stopped_cacm):
            os.makedirs(stopped_cacm, 0755)

        stop_words = self.get_stop_words()
        os.chdir(clean_cacm)

        for eachfile in glob.glob('*.html'):
            print eachfile
            content = open(eachfile).read()
            content = content.split()
            stopped_content = [x for x in content if x not in stop_words]
            final_content = " ".join(stopped_content)

            clean_file = open(os.path.join(stopped_cacm, eachfile), 'w')
            clean_file.write(final_content)
            clean_file.close()

    def get_stop_words(self):
        with open('common_words') as f:
            stop_words = f.read().splitlines()

        return stop_words

    def build_stopped_inverted_index(self):
        r = Retriever()
        stopped_corpus = r.build_index(folder='stopped')
        stopped_inv_index = stopped_corpus[0]
        stopped_docs = stopped_corpus[1]
        return stopped_inv_index, stopped_docs


class Stemmer:

    def __init__(self):
        self.stemmed_data = self.build_stemmed_data()
        return

    def build_stemmed_data(self):
        with open('cacm_stem.txt') as f:
            data = f.read()
        data = data.split('#')
        data = [s.replace('\n', ' ') for s in data]
        data = data[1:]
        stemmed_data = {}
        for each in data:
            each_doc = each.split()
            idd = each_doc[0]
            content = each_doc[1:]
            last = 0
            for i, v in enumerate(reversed(content)):
                if v == 'am' or v == 'pm':
                    last = len(content) - i - 1
                    break
            content = content[0:last+1]

            doc_content = " ".join(content)
            idd = str(idd)
            diff = 4 - len(idd)
            z = diff * '0'
            idd = z+idd
            docid = 'CACM-'+idd
            stemmed_data[docid] = doc_content

        return stemmed_data

    def build_stemmed_index(self):
        inverted_index = {}
        stemmed_data = self.stemmed_data
        for eachfile in stemmed_data:
            docid = eachfile
            content_as_list = stemmed_data[eachfile].split()
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
        stepped_inv_index = inverted_index
        return stepped_inv_index