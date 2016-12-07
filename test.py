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
        fnewname = eachfile[:-4] + '_lucene.txt'
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