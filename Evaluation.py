#! /usr/bin/env python

import os
from FileAccess import FileAccess

class Evaluation:

    def __init__(self):
        return

    def evaluate(self, file_name, rank_list):
        fa = FileAccess()
        scores = fa.read_score_file(file_name)
        relevant_data = fa.get_relevance_data()
        pr_results = []
        ap_results = []
        mrr = []
        p_at_k = {}
        for each in rank_list:
            p_at_k[each] = []
        for each in scores:
            ap = 0
            if each in relevant_data:
                relevant_files = relevant_data[each]
            else:
                continue
            data = scores[each]
            total_retrieved = 1
            total_relevant_retrieved = 0
            for eachdata in data:
                qid = each
                rank = data.index(eachdata) + 1
                docid = eachdata[0]
                doc_score = eachdata[1]
                if docid in relevant_files:
                    if total_relevant_retrieved == 0:
                        mrr.append(1.0/rank)
                    total_relevant_retrieved += 1
                relevance = 1 if docid in relevant_files else 0
                precision = float(total_relevant_retrieved)/total_retrieved
                if rank in rank_list:
                    tup = (qid, precision)
                    p_at_k[rank].append(tup)
                if relevance:
                    ap += precision
                recall = float(total_relevant_retrieved)/len(relevant_files)
                total_retrieved += 1
                tup = (qid, rank, docid, doc_score, str(relevance), precision, recall)
                pr_results.append(tup)
            if total_relevant_retrieved != 0:
                avg_p = float(ap)/total_relevant_retrieved
            else:
                avg_p = 0
            ap_results.append(avg_p)

        mean_avg_pr = sum(ap_results)/len(relevant_data)
        mean_rr = sum(mrr)/len(relevant_data)

        phase2_evaluation = os.path.join(os.getcwd(), 'evaluation_phase2')

        pre = 'ashok'

        if not os.path.exists(phase2_evaluation):
            os.makedirs(phase2_evaluation, 0755)

        for each in p_at_k:
            pk_file_name = pre + '_p@k'+str(each)+'.txt'
            pk_file = open(os.path.join(phase2_evaluation, pk_file_name), 'w')
            for e in p_at_k[each]:
                pk_file.write('{} {}\n'.format(e[0], e[1]))
            pk_file.close()

        return
        file_name = 'ashok'
        mrr_filename = file_name + '_mrr.txt'
        pr_filename = file_name + '_precision_recall.txt'
        map_filename = file_name + '_map_results.txt'

        mrr_file = open(os.path.join(phase2_evaluation, mrr_filename), 'w')
        mrr_file.write(str(mean_rr))
        mrr_file.close()

        map_file = open(os.path.join(phase2_evaluation, map_filename), 'w')
        map_file.write('{} {}\n'.format(str(mean_avg_pr)))
        map_file.close()

        pr_file = open(os.path.join(phase2_evaluation, pr_filename), 'w')
        for e in pr_results:
            pr_file.write("{} {} {} {} {} {} {}\n".format(e[0], e[1], e[2], e[3], e[4], round(e[5], 3), round(e[6], 3)))
        pr_file.close()

        return
