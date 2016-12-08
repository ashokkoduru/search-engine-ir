import os


class Evaluation:

    def __init__(self):
        return

    def read_file(self, file_name):
        with open(file_name) as f:
            data = f.read().splitlines()

        data = [s.split() for s in data]
        scores = {}
        for each in data:
            d = (each[2], each[4])
            scores.setdefault(int(each[0]), []).append(d)
        return scores

    def get_relevance_data(self):
        relevance_data = {}
        with open("cacm.rel") as content:
            data = content.read().splitlines()
        data = [s.split() for s in data]
        for qid in data:
            relevance_data.setdefault(int(qid[0]), []).append(qid[2])
        return relevance_data

    def evaluate(self, file_name):
        scores = self.read_file(file_name=file_name)
        relevant_data = self.get_relevance_data()
        pr_results = []
        map_results = {}
        mrr = []
        total_r = 0
        for each in scores:
            map = 0
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
                        total_r += 1
                    total_relevant_retrieved += 1
                relevance = 1 if docid in relevant_files else 0
                precision = float(total_relevant_retrieved)/total_retrieved
                if relevance:
                    map += precision
                recall = float(total_relevant_retrieved)/len(relevant_files)
                total_retrieved += 1
                tup = (qid, rank, docid, doc_score, str(relevance), precision, recall)
                pr_results.append(tup)
            if total_relevant_retrieved != 0:
                mean_avg_p = float(map)/total_relevant_retrieved
            else:
                mean_avg_p = 0
            map_results[each] = mean_avg_p
        if total_r != 0:
            mean_rr = sum(mrr)/total_r
        else:
            mean_rr = 'Does not exist'
        phase2_evaluation = os.path.join(os.getcwd(), 'evaluation_phase2')

        if not os.path.exists(phase2_evaluation):
            os.makedirs(phase2_evaluation, 0755)

        mrr_filename = file_name+ '_mrr.txt'
        pr_filename = file_name + '_precision_recall.txt'
        map_filename = file_name + '_map_results.txt'

        mrr_file = open(os.path.join(phase2_evaluation, mrr_filename), 'w')
        mrr_file.write(str(mean_rr))
        mrr_file.close()

        map_file = open(os.path.join(phase2_evaluation, map_filename), 'w')
        for each in map_results:
            map_file.write('{} {}\n'.format(str(each), str(map_results[each])))
        map_file.close()

        pr_file = open(os.path.join(phase2_evaluation, pr_filename), 'w')
        for e in pr_results:
            pr_file.write("{} {} {} {} {} {} {}\n".format(e[0], e[1], e[2], e[3], e[4], round(e[5], 3), round(e[6], 3)))
        pr_file.close()

        return
