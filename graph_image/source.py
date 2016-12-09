import matplotlib.pyplot as plot
def plot_graph(file, img_name):
    precision_values = {}
    recall_values = {}
    query_values = {}
    with open(file) as content:
        data = content.read().splitlines()
    data = [s.split() for s in data]
    # print data
    i = 0
    for pid in data:
        precision_values.setdefault(int(pid[0]), []).append(pid[5])
    # print precision_values
    for rid in data:
        recall_values.setdefault(int(rid[0]),[]).append(rid[6])
    # print recall_values
    for qid in data:
        query_values.setdefault(int(qid[0]),[]).append(qid[5:])
    # print query_values

    for qu_id, val in query_values.items():
        p_val = (precision_values[qu_id])
        r_val = (recall_values[qu_id])

        plot.plot(r_val,p_val)
        plot.suptitle(graph_name)
        plot.xlabel("Recall")
        plot.ylabel("Precision")

    plot.savefig(img_name + '.png')
    plot.clf()

file_name = raw_input("Enter the text file name: ")
graph_name = file_name
file_name = file_name + '.txt'


plot_graph(file_name,graph_name)