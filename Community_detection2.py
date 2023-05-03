from tkinter import ttk
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from cdlib import algorithms, evaluation,viz, NodeClustering
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def selection_nodestab():
    #print(combobox_nodestab.get())
    frame = Frame(root)
    frame.pack()
    frame.place(x=400,y=100,width=500,height=500)
    fig, ax = plt.subplots()
    if(combobox_nodestab.get()=="Degree"):
        Adjusting_node_size_based_on_node_degree()
    elif(combobox_nodestab.get()=="In-Degree"):
        Adjusting_node_size_based_on_node_in_degree()
    elif(combobox_nodestab.get()=="Out-Degree"):
        Adjusting_node_size_based_on_node_out_degree()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def selection_edgestab():
    #print(combobox_edgestab.get())
    frame = Frame(root)
    frame.pack()
    frame.place(x=400, y=100, width=500, height=500)
    fig, ax = plt.subplots()
    if(combobox_edgestab.get()=="Weight"):
        Adjusting_edge_width_based_on_edge_weight()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def Adjusting_node_size_based_on_node_degree():
    nx.draw(G, pos, with_labels=True, node_size=[(degree + 1) * 50 for (node, degree) in nx.degree(G)])
    #plt.show()

def Adjusting_node_size_based_on_node_in_degree():
    nx.draw(G,pos, with_labels=True, node_size=[(degree+1) * 50 for (node, degree) in G.in_degree()])
    #plt.show()

def Adjusting_node_size_based_on_node_out_degree():
    nx.draw(G,pos, with_labels=True, node_size=[(degree+1) * 50 for (node, degree) in G.out_degree()])
    #plt.show()

def Adjusting_edge_width_based_on_edge_weight():
    nx.draw(G,pos, node_size=50, with_labels=True, width=[edge[2] for edge in G.edges(data='Weight')])
    #plt.show()

def community_detection_evaluation(ev,communities):
    ##modularity (Internal evaluation)
    if(ev == "modularity"):
        com = []
        for c in communities.communities:
            com.append(set(c))
            #print(set(c))
        mod = nx.community.modularity(G,com)
        eval = mod
        #print(mod)

    ##NMI (external evaluation)
    elif(ev == "nmi"):
        #first method => comparing different graph partition to assess their resemblance
        leiden_communities = algorithms.leiden(G)
        #print(len(leiden_communities.communities))
        NMI = evaluation.normalized_mutual_information(communities,leiden_communities)
        #print(NMI)
        #second method applying nmi by using a class attribute
        #class_communities = community_detection("Class")
        #NMI = evaluation.normalized_mutual_information(communities, class_communities)
        #print(NMI)
        eval = NMI

    ##Internal edge distance (Internal evaluation)
    elif(ev == "internal edge denisty"):
        internal_edge_denisty = evaluation.internal_edge_density(G,communities,summary=False)
        eval = internal_edge_denisty
        #print(internal_edge_denisty)

    ##Average distance (Internal evaluation)
    #The average distance of a community is defined average path length across all possible pair of nodes composing it
    elif(ev == "avgdist"):
        avg_dist = evaluation.avg_distance(G,communities,summary=False)
        eval = avg_dist
        #print(avg_dist)
    return eval

def community_detection(algorithm):
    if(algorithm == "louvain"):
        communities = algorithms.louvain(G)

    elif(algorithm == "Class"):
        classes = nodes['Class'].unique()
        print(classes)
        comm = []
        for c in classes:
            selected_nodes = nodes[nodes['Class'] == c]
            ids = selected_nodes['ID'].tolist()
            print(c)
            print(ids)
            comm.append(ids)
        print(comm)
        communities = NodeClustering(comm,G)

    #viz.plot_network_clusters(G, communities, pos, plot_labels=True)
    #plt.show()
    #print(communities.communities)
    return communities


root = Tk()
root.title('Appearance')
root.geometry("1000x700")
tabControl = ttk.Notebook(root)
nodes_tab = ttk.Frame(tabControl)
edges_tab = ttk.Frame(tabControl)
tabControl.add(nodes_tab, text='Nodes')
tabControl.add(edges_tab, text='Edges')
tabControl.pack()
tabControl.place(x=0,y=0,width=400,height=300)

edgesfile = input("Edges' csv file to import: ")
nodesfile = input("Nodes' csv file to import: ")
graphtype = int(input("Graph Type: 1- Directed  2- Undirected"))
edges = pd.read_csv(edgesfile)
nodes = pd.read_csv(nodesfile)

if 'Weight' in edges:
    edgesWithWeights = edges

else:
    edgesWithWeights = edges.groupby(['Source', 'Target']).size().reset_index(name='Weight')
    edgesWithWeights.to_csv(index=False)

if graphtype == 2:
    G = nx.from_pandas_edgelist(edgesWithWeights, 'Source', 'Target','Weight', create_using=nx.Graph())
    combobox_nodestab = ttk.Combobox(nodes_tab,values=["Degree"])
else:
    G = nx.from_pandas_edgelist(edgesWithWeights, 'Source', 'Target','Weight', create_using=nx.DiGraph())
    combobox_nodestab = ttk.Combobox(nodes_tab, values=["Degree","In-Degree","Out-Degree"])

#print(len(list(G.nodes)))
G.add_nodes_from(nodes['ID'].tolist())
#print(len(list(G.nodes)))
pos = nx.spring_layout(G)

ttk.Label(nodes_tab,text="Adjusting node size based on:").place(x=20,y=60)
combobox_nodestab.place(x=75,y=100)
button_nodestab = ttk.Button(nodes_tab,text="Apply",command=selection_nodestab)
button_nodestab.place(x=100,y=140)

ttk.Label(edges_tab,text="Adjusting edge thickness based on:").place(x=20,y=60)
combobox_edgestab = ttk.Combobox(edges_tab,values=["Weight"])
combobox_edgestab.place(x=75,y=100)
button_edgestab = ttk.Button(edges_tab,text="Apply",command=selection_edgestab)
button_edgestab.place(x=100,y=140)

#communities = community_detection("louvain")
#community_detection_evaluation("modularity",communities)



root.mainloop()



