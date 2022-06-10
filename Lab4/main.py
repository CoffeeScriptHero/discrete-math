import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
w = 900
h = 900
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.title("Евристичний алгоритм розфарбування")

option = 1309 % 6 + 1


def generate_graph():
    # G = nx.Graph()
    # G.add_edges_from([(1, 2), (1, 6), (6, 2), (2, 3), (2, 7),
    #                   (3, 4), (3, 7), (7, 8), (8, 9), (8, 10),
    #                   (3, 9), (4, 5), (5, 10), (9, 5)])
    G = nx.circulant_graph(12, [4])
    pos = nx.spring_layout(G, k=15, seed=70)
    return G, pos


def draw_graph(G, pos, color_map=["lightgrey"], x=330, y=-60):
    figure = plt.Figure(figsize=(6, 5.3), dpi=100)
    a = figure.add_subplot(111)
    nx.draw(G, pos, ax=a, with_labels=True, node_size=550, node_color=color_map)
    figure.patch.set_facecolor('#F0F0F0')
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(x=x, y=y)


def create_graph():
    G, pos = generate_graph()
    draw_graph(G, pos)


def paint_graph():
    global nodes_lbl, edges_lbl, chromatic_lbl
    G, pos = generate_graph()
    colors = ["yellow", "red", "lightblue", "grey", "brown", "orange", "green", "purple", "black", "white"]
    sorted_pairs = [(node, deg) for (node, deg) in G.degree()]
    sorted_pairs.sort(key=lambda tup: tup[1], reverse=True)
    nodes = [node for (node, deg) in sorted_pairs]
    nodes_colors = {n: -1 for n in G.nodes()}

    for c in range(len(nodes)):
        x = c
        while True:
            if x == len(nodes): break
            if nodes_colors[nodes[x]] == -1:
                nodes_colors[nodes[x]] = c
                break
            else: x += 1
        for j in nodes:
            if nodes_colors[j] != -1: continue
            adjacent_nodes = []
            for k, v in G.edges():
                if k == j: adjacent_nodes.append(v)
                if v == j: adjacent_nodes.append(k)
            is_adjacent = False
            for node in adjacent_nodes:
                if nodes_colors[node] == c: is_adjacent = True
            nodes_colors[j] = c if not(is_adjacent) else -1

    color_map = [colors[nodes_colors[i]] for i in G.nodes()]
    draw_graph(G, pos, color_map, 330, 390)
    nodes_lbl.configure(text=f'Кількість вершин: {len(nodes)}')
    edges_lbl.configure(text=f'Кількість ребер: {len(G.edges())}')
    chromatic_lbl.configure(text=f'Хроматичне число: {len(set(nodes_colors.values()))}')
    create_graph()


create_graph()

Label(root, text="Козаренко Денис", font=("Arial", 20)).place(x=15, y=30)
Label(root, text="Група ІО-13", font=("Arial", 20)).place(x=15, y=70)
Label(root, text="Номер у списку групи: 9", font=("Arial", 20)).place(x=15, y=105)
Label(root, text=f"Номер варіанту: {option}", font=("Arial", 20)).place(x=15, y=140)
alg_lbl = Label(root, text="Евристичний \n алгоритм", font=("Arial", 20))
alg_lbl.place(x=15, y=230)
Button(root, text="Показати граф", command=create_graph, font=("Arial", 18)).place(x=30, y=400)
Button(root, text="Розфарбувати", command=paint_graph, font=("Arial", 18)).place(x=30, y=480)
nodes_lbl = Label(root, font=("Arial", 18))
nodes_lbl.place(x=25, y=600)
edges_lbl = Label(root, font=("Arial", 18))
edges_lbl.place(x=25, y=640)
chromatic_lbl = Label(root, font=("Arial", 18))
chromatic_lbl.place(x=25, y=680)

root.mainloop()

