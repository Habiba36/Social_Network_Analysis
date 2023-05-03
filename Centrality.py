from tkinter import *
# from PIL import ImageTk ,Image
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

root = Tk()
root.title("mini gephi")
root.geometry("1000x1000")

type_of_graph = StringVar()
nodes_path = ""
edges_path = ""


def upload_file():
    new_window = Toplevel(root)
    new_window.title("upload files")
    new_window.geometry("500x500")

    def upload_Btn(button_id):
        # filename = filedialog.askopenfilename(initialdir="/home/rengo/Downloads", title="Select A File", filetypes=(("jpg files", ".jpg"),("all files", ".*")))
        # print(f" {button_id} : {filename}")
        global nodes_path
        global edges_path
        if (button_id == "nodes"):
            nodes_path = filedialog.askopenfilename(initialdir="/home/rengo/Downloads", title="Select A File",
                                                    filetypes=(("jpg files", ".jpg"), ("all files", ".*")))

        else:
            edges_path = filedialog.askopenfilename(initialdir="/home/rengo/Downloads", title="Select A File",
                                                    filetypes=(("jpg files", ".jpg"), ("all files", ".*")))

    def done():
        new_window.destroy()

        print("nodes :", nodes_path)
        print("edges :", edges_path)
        print("type of graph :", type_of_graph.get())

        # plot graph inside the window
        frame = Frame(root)
        frame.pack()
        fig, ax = plt.subplots()

        edges = pd.read_csv(edges_path)
        G = nx.from_pandas_edgelist(edges, 'Source', 'Target', create_using=nx.Graph())
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_size=50, with_labels=True)

        # Create a Matplotlib canvas and embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def when_change(value):
        print(value)

    Button(new_window, text="upload nodes", name="nodes", command=lambda: upload_Btn("nodes")).pack()
    Button(new_window, text="upload edges", name="edges", command=lambda: upload_Btn("edges")).pack()

    Label(new_window, text="directed or undirected:").pack()

    directed_button = Radiobutton(new_window, text="Directed", variable=type_of_graph, value="directed",
                                  command=lambda: when_change(type_of_graph.get()))
    directed_button.pack()

    undirectd_button = Radiobutton(new_window, text="Undirected", variable=type_of_graph, value="undirected",
                                   command=lambda: when_change(type_of_graph.get()))
    undirectd_button.pack()

    Button(new_window, text="Done", command=done).pack()


def girven_newman():
    pass


def louvain():
    pass

def closeness_centrality():
    window = tk.Tk()
    window.title("Closeness Centrality")
    window.geometry('600x600')

    # add a label
    label = tk.Label(window, text='Filter by closeness centrality:')
    label.pack()

    # add an entry box
    entry_box = tk.Entry(window)
    entry_box.pack()

    # add a button
    def filter_nodes():
        centrality_threshold = float(entry_box.get())
        filtered_nodes = [node for node, centrality in nx.closeness_centrality(graph).items() if
                          centrality > centrality_threshold]
        display(filtered_nodes)
        plot_graph(filtered_nodes)

    button = tk.Button(window, text='Filter', command=filter_nodes)
    button.pack()

    # add a canvas
    canvas = tk.Canvas(window)
    canvas.pack()

    # generate the graph
    df = pd.read_csv(edges_path)
    graph = nx.Graph()
    for i, row in df.iterrows():

        graph.add_edge(row['Source'], row['Target'])

    nx.draw(graph, with_labels=True)

    def plot_graph(filtered_nodes):
        window1 = tk.Tk()
        window1.title("Closeness Centrality Graph")
        window1.geometry('700x700')
        frame = Frame(window1)
        frame.pack()
        fig, ax = plt.subplots(figsize=(10, 10))
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue')
        nx.draw_networkx_nodes(graph, pos, node_color='red', nodelist=filtered_nodes)
        nx.draw_networkx_edges(graph, pos, alpha=0.5)
        nx.draw_networkx_labels(graph, pos)

        # Create a Matplotlib canvas and embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        window1.mainloop()

    def display(filtered_nodes):
        listbox = tk.Listbox(window)
        for item in filtered_nodes:
            listbox.insert(tk.END, item)
        listbox.pack()



    # start the tkinter main loop
    window.mainloop()

def betweenness_centrality():
    window = tk.Tk()
    window.title("betweenness Centrality")
    window.geometry('600x600')

    # add a label
    label = tk.Label(window, text='Filter by betweenness centrality:')
    label.pack()

    # add an entry box
    entry_box = tk.Entry(window)
    entry_box.pack()

    # add a button
    def filter_nodes():
        centrality_threshold = float(entry_box.get())
        filtered_nodes = [node for node, centrality in nx.betweenness_centrality(graph).items() if
                          centrality > centrality_threshold]
        display(filtered_nodes)
        plot_graph(filtered_nodes)

    button = tk.Button(window, text='Filter', command=filter_nodes)
    button.pack()

    # add a canvas
    canvas = tk.Canvas(window)
    canvas.pack()

    # generate the graph
    df = pd.read_csv(edges_path)
    graph = nx.Graph()
    for i, row in df.iterrows():
        graph.add_edge(row['Source'], row['Target'])
    nx.draw(graph, with_labels=True)

    def plot_graph(filtered_nodes):
        window1 = tk.Tk()
        window1.title("Betweenness Centrality Graph")
        window1.geometry('700x700')
        frame = Frame(window1)
        frame.pack()
        fig, ax = plt.subplots(figsize=(10, 10))
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue')
        nx.draw_networkx_nodes(graph, pos, node_color='red', nodelist=filtered_nodes)
        nx.draw_networkx_edges(graph, pos, alpha=0.5)
        nx.draw_networkx_labels(graph, pos)

        # Create a Matplotlib canvas and embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        window1.mainloop()

    def display(filtered_nodes):
        listbox = tk.Listbox(window)
        for item in filtered_nodes:
            listbox.insert(tk.END, item)
        listbox.pack()

    # start the tkinter main loop
    window.mainloop()
def degree_centrality():
    window = tk.Tk()
    window.title("degree Centrality")
    window.geometry('600x600')

    # add a label
    label = tk.Label(window, text='Filter by degree centrality:')
    label.pack()

    # add an entry box
    entry_box = tk.Entry(window)
    entry_box.pack()

    # add a button
    def filter_nodes():
        centrality_threshold = float(entry_box.get())
        filtered_nodes = [node for node, centrality in nx.degree_centrality(graph).items() if
                          centrality > centrality_threshold]
        display(filtered_nodes)
        plot_graph(filtered_nodes)

    button = tk.Button(window, text='Filter', command=filter_nodes)
    button.pack()

    # add a canvas
    canvas = tk.Canvas(window)
    canvas.pack()

    # generate the graph
    df = pd.read_csv(edges_path)
    graph = nx.Graph()
    for i, row in df.iterrows():
        graph.add_edge(row['Source'], row['Target'])
    nx.draw(graph, with_labels=True)

    def plot_graph(filtered_nodes):
        window1 = tk.Tk()
        window1.title("Degree Centrality Graph")
        window1.geometry('700x700')
        frame = Frame(window1)
        frame.pack()
        fig, ax = plt.subplots(figsize=(10, 10))
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue')
        nx.draw_networkx_nodes(graph, pos, node_color='red', nodelist=filtered_nodes)
        nx.draw_networkx_edges(graph, pos, alpha=0.5)
        nx.draw_networkx_labels(graph, pos)

        # Create a Matplotlib canvas and embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        window1.mainloop()

    def display(filtered_nodes):
        listbox = tk.Listbox(window)
        for item in filtered_nodes:
            listbox.insert(tk.END, item)
        listbox.pack()

    # start the tkinter main loop
    window.mainloop()
def PageRank():
    window = tk.Tk()
    window.title("Page Rank")
    window.geometry('600x600')

    # add a label
    label = tk.Label(window, text='Highest Page Rank')
    label.pack()

    # add a button
    def filter_nodes():
        page_rank=nx.pagerank(graph)
        max_pr = max(page_rank.values())
        filtered_nodes = [node for node, pagerank in nx.pagerank(graph).items() if
                          pagerank==max_pr]
        display(filtered_nodes)
        plot_graph(filtered_nodes)

    button = tk.Button(window, text='Display', command=filter_nodes)

    button.pack()
    # add a canvas
    canvas = tk.Canvas(window)
    canvas.pack()

    # generate the graph
    df = pd.read_csv(edges_path)
    graph = nx.Graph()
    for i, row in df.iterrows():
        graph.add_edge(row['Source'], row['Target'])
    nx.draw(graph, with_labels=True)

    def plot_graph(filtered_nodes):
        window1 = tk.Tk()
        window1.title("Page Rank Graph")
        window1.geometry('700x700')
        frame = Frame(window1)
        frame.pack()
        fig, ax = plt.subplots(figsize=(10, 10))
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue')
        nx.draw_networkx_nodes(graph, pos, node_color='red', nodelist=filtered_nodes)
        nx.draw_networkx_edges(graph, pos, alpha=0.5)
        nx.draw_networkx_labels(graph, pos)

        # Create a Matplotlib canvas and embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        window1.mainloop()


    def display(filtered_nodes):

        messagebox.showinfo("Node", filtered_nodes)






    # start the tkinter main loop
    window.mainloop()

# menu
my_menu = Menu(root)
root.config(menu=my_menu)


file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="upload files", command=upload_file)
file_menu.add_command(label="Exit", command=root.quit)

community_detection = Menu(my_menu)
my_menu.add_cascade(label="community detection ", menu=community_detection)
community_detection.add_command(label="girven newman", command=girven_newman)
community_detection.add_command(label="louvain ", command=louvain)

measure_centrality = Menu(my_menu)
my_menu.add_cascade(label="measure centrality", menu=measure_centrality)
measure_centrality.add_command(label="degree centrality", command=degree_centrality)
measure_centrality.add_command(label="betweenness centrality", command=betweenness_centrality)
measure_centrality.add_command(label="closeness centrality ", command=closeness_centrality)

Page_Rank = Menu(my_menu)
my_menu.add_cascade(label="Page Rank", menu=Page_Rank)
Page_Rank.add_command(label="Page Rank", command=PageRank)
root.mainloop()