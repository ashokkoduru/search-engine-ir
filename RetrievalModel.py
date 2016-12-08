from collections import Counter
import math


class TfIdf:

    def __init__(self, inverted_index, total_corpus):
        self.inverted_index = inverted_index
        self.total_corpus = total_corpus
        return

    def get_tf_idf(self, query):
        query_terms = query.split()
        corpus_content = self.total_corpus
        tf_idf_scores = {}
        total_files = len(corpus_content)
        for eachfile in corpus_content:
            docid = eachfile
            tf_idf_file = 0
            for each_query_term in query_terms:
                if each_query_term not in self.inverted_index:
                    continue
                tf_term = corpus_content[eachfile].count(each_query_term)/float(len(corpus_content[eachfile]))
                idf_term = math.log(float(total_files)/len(self.inverted_index[each_query_term]))
                tf_idf_file += tf_term * idf_term
            tf_idf_scores[docid] = tf_idf_file
        return tf_idf_scores


class CosineSimilarity:

    def __init__(self, inverted_index, total_corpus):
        self.inverted_index = inverted_index
        self.total_corpus = total_corpus
        return

    def get_cosine_similarity(self, query):
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
            if each not in self.inverted_index:
                continue
            doclist = inv_index[each]
            for d in doclist:
                docset.append(d)
        docset = list(set(docset))
        for eachfile in total_corpus:
            docid = eachfile
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
                if each_query_term not in self.inverted_index:
                    continue
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
        return cosine_similarity


class BM25:

    def __init__(self, inverted_index, total_corpus, relevance_data):
        self.inverted_index = inverted_index
        self.total_corpus = total_corpus
        self.relevance_data = relevance_data
        self.avdl = self.get_avdl()
        self.k1 = 1.2
        self.k2 = 200
        self.b = 0.75

    def get_avdl(self):
        total_tokens = 0
        for eachdoc in self.total_corpus:
            total_tokens += len(eachdoc)

        return total_tokens/len(self.total_corpus)

    def calculate_bm25(self, query, query_id):
        query_terms = query.split()
        total_corpus = self.total_corpus
        bm25 = {}
        for eachfile in total_corpus:
            word_count = dict(Counter(total_corpus[eachfile]))
            docid = eachfile
            bm25_value = 0
            doc_part = (1 - self.b) + ((self.b*len(total_corpus[docid]))/self.avdl)
            K = self.k1 * doc_part
            for each_query_term in query_terms:
                if each_query_term not in total_corpus[docid]:
                    continue
                else:
                    if query_id not in self.relevance_data:
                        R = 0
                        ri = 0
                    else:
                        R = len(self.relevance_data[query_id])
                        reli = 0
                        for each in self.relevance_data[query_id]:
                            l = each.split('-')
                            diff = 4-len(l[1])
                            z = diff*'0'
                            l[1] = z+l[1]
                            each = "-".join(l)
                            if each_query_term in total_corpus[each]:
                                reli += 1
                        ri = reli
                    fi = word_count[each_query_term]
                    qfi = query_terms.count(each_query_term)
                    ni = len(self.inverted_index[each_query_term])
                    document_factor = ((self.k1 + 1)*fi)/(K + fi)
                    query_factor = ((self.k2 + 1)*qfi)/(self.k2 + qfi)
                    n1 = ((ri + 0.5)/(R - ri + 0.5))
                    n2 = ((ni - ri + 0.5)/(len(total_corpus) - ni - R + ri + 0.5))
                    relevance_factor = n1 / n2
                    bm25_value += math.log(relevance_factor * document_factor * query_factor)
            bm25[eachfile] = bm25_value
        return bm25
