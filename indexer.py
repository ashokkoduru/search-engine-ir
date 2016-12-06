#! /usr/bin/env python

# Author : Ashok, Sravanthi and Frenia
# Date   : 6th December 2016
# Task   : IR Final Project

from collections import Counter
import os
import string
import glob
import operator
import math


class Indexer:

    def __init__(self):
        self.docdict = {}
        return

    def build_docid_dict(self, ret=False):
        cwd = os.getcwd()
        cacm = os.path.join(cwd, 'cacm')
        os.chdir(cacm)
        for eachfile in glob.glob("*.html"):
            docid = eachfile[5:-5]
            self.docdict[eachfile] = docid

        if ret:
            return self.docdict

    def build_n_gram_index(self):
        self.build_docid_dict()
        inverted_index = {}
        # token_count = {}
        for eachfile in glob.glob('*.html'):
            print eachfile
            file_content = open(eachfile)
            content = file_content.read()
            content_as_list = content.split()
            # token_count[fname] = len(content_as_list)
            word_count = dict(Counter(content_as_list))
            for token in content_as_list:
                if token not in inverted_index:
                    temp = dict()
                    temp[self.docdict[eachfile]] = word_count[token]
                    inverted_index[token] = temp
                else:
                    temp = inverted_index[token]
                    temp[self.docdict[eachfile]] = word_count[token]
                    inverted_index[token] = temp

        print inverted_index

    def create_tf_table(self, n, filesave=True, stopword_flag=False):
        inv_index = self.build_n_gram_index(n)
        tf_dict = {}
        for token in inv_index:
            tf_dict[token] = 0
            for dt in inv_index[token]:
                tf_dict[token] += inv_index[token][dt]
        if stopword_flag:
            return inv_index, tf_dict
        sorted_tf_dict = sorted(tf_dict.items(), key=operator.itemgetter(1), reverse=True)
        os.chdir("..")
        if filesave:
            f = open(str(n)+'_gram_tf_table.txt', 'w')
            for each in sorted_tf_dict:
                f.write('{} {}\n'.format(each[0], each[1]))
            f.close()

    def create_df_table(self, n):
        inv_index = self.build_n_gram_index(n)
        lexic_tokens = sorted(inv_index)
        df_values = []
        for token in lexic_tokens:
            d_lst = []
            for each in inv_index[token]:
                d_lst.append(each)
            df = len(d_lst)
            tup = (token, d_lst, df)
            df_values.append(tup)
        os.chdir("..")
        f = open(str(n)+'_gram_df_table.txt', 'w')
        for each in df_values:
            f.write('{} {} {}\n'.format(each[0], each[1], each[2]))
        f.close()

    def stopwords(self):
        tf_table = self.create_tf_table(1, stopword_flag=True)
        (inv_index, tf_dict) = (tf_table[0], tf_table[1])
        total_terms = sum(tf_dict.values())
        print total_terms
        stopword_tf = {}
        print len(self.docdict)
        for each in inv_index:
            tf = float(tf_dict[each])/total_terms
            idf = math.log(float(len(self.docdict))/len(inv_index[each]), 2)
            stopword_tf[each] = idf
        sorted_sw_dict = sorted(stopword_tf.items(), key=operator.itemgetter(1), reverse=False)
        os.chdir('..')
        f = open('stop_word_table.txt', 'w')
        for each in sorted_sw_dict:
            f.write('{} {}\n'.format(each[0], each[1]))
        f.close()

    def find_ngrams(self, input_list, n):
        zip_list = zip(*[input_list[i:] for i in range(n)])
        gram_list = []
        for each in zip_list:
            m = list(each)
            m = ' '.join(m)
            gram_list.append(m)
        return gram_list

    def save_docids(self):
        self.build_docid_dict()
        f = open('DocIDs.txt', 'w')
        for each in self.docdict:
            f.write('{} {}\n'.format(each, str(self.docdict[each])))
        f.close()


def hw3_tasks():
    ind = Indexer()
    # This method builds the clean corpus from raw corpus
    # ind.build_parsed_corpus()
    # print ind.parse_page(s)
    # ind.save_docids()
    ind.build_n_gram_index()

    # ind.build_docid_dict()
    # ####### Change this value to respective value to see unigram, bigram and trigram data
    # n = 3
    #
    # ####### Change this to False if the plot should not be shown. False by default
    # plot_flag = False

    # ind.create_tf_table(n, plot=plot_flag, filesave=True)
    # ind.create_df_table(n)
    # ind.stopwords()
    return

hw3_tasks()
