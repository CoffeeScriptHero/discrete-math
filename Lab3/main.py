import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from math import inf
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
w = 900
h = 800
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.title("Алгоритм Левіта")

option = 1309 % 10 + 1

cost_label = Label(font=("Arial", 18))
cost_label.place(x=50, y=500)


def restore_path(tup):
    return (*restore_path(tup[1]), tup[0]) if tup else ()


def levit(gr, start, end):
        dist = defaultdict(lambda: inf)
        dist[start] = 0
        path = {start: (start, ())}
        m0 = set()  # відстань вже обчислено (можливо, не до кінця)
        m1, m1_urg = [start], []  # відстань обчислюється
        m2 = set(node for node in gr.nodes())  # відстань ще не обчислено

        def relax(u, v, w):
            if dist[v] > dist[u] + w['weight']:
                dist[v] = dist[u] + w['weight']
                path[v] = (v, path[u])
                return True
            return False

        while m1 or m1_urg:
            u = m1_urg.pop() if m1_urg else m1.pop()
            next_nodes = [(v, w) for (k, v, w) in gr.edges(data=True) if k == u]
            for (v, w) in next_nodes:
                if v in m2:
                    m1.append(v)
                    m2.discard(v)
                    relax(u, v, w)
                elif v in m1:
                    relax(u, v, w)
                elif v in m0 and relax(u, v, w):
                    m1_urg.append(v)
                    m0.discard(v)
                    dist[v] = dist[u] + w['weight']
            m0.add(u)
        return dist[end], list(restore_path(path[end]))


def generate_graph():
    global G, pos, width, colors
    G = nx.DiGraph()
    G.add_weighted_edges_from(
        [(0, 6, 5.0), (0, 2, 2.0), (0, 1, 1.0), (6, 4, 4.0),
         (2, 4, 8.0), (1, 7, 1.0), (1, 3, 2.0), (2, 3, 7.0), (4, 3, 3.0),
         (3, 5, 3.0), (7, 5, 9.0), (3, 8, 9.0), (5, 8, 8.0)])
    pos = nx.spring_layout(G, k=15, seed=70)
    for u, v in G.edges():
        G[u][v]['color'] = 'black'
        G[u][v]['width'] = 1
    colors = [G[u][v]['color'] for u, v in G.edges()]
    width = [G[u][v]['width'] for u, v in G.edges()]
    return G, pos, colors, width


def find_shortest_way(start, end):
    generate_graph()
    global G, pos, width, colors
    try:
        cost, path = levit(G, int(start), int(end))
    except:
        cost_label.configure(text="Некоректні дані")
        cost_label.configure(fg="red")
        return
    for i in range(len(path)):
        if i < len(path) - 1:
            G[path[i]][path[i + 1]]['color'] = 'green'
            G[path[i]][path[i + 1]]['width'] = 2
    colors = [G[u][v]['color'] for u, v in G.edges()]
    width = [G[u][v]['width'] for u, v in G.edges()]
    color_map = ['red' if node in path else 'purple' for node in G]
    print(color_map)
    draw_graph(G, pos, colors, width, color_map)
    cost_label.configure(text=f"Ціна шляху: {cost}")


def draw_graph(G, pos, colors, width, color_map):
    cost_label.configure(fg="black")
    figure = plt.Figure(figsize=(6, 6), dpi=112)
    a = figure.add_subplot(111)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=a, edge_labels=labels, label_pos=0.4, verticalalignment='bottom',
                                 horizontalalignment='left')
    nx.draw(G, pos, ax=a, with_labels=True, edge_color=colors, node_size=550, node_color=color_map, width=width)
    figure.patch.set_facecolor('#F0F0F0')
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(x=275, y=160)


def create_graph():
    cost_label.configure(text="")
    G, pos, colors, width = generate_graph()
    draw_graph(G, pos, colors, width, ["purple"])


create_graph()

Label(root, text="Козаренко Денис", font=("Arial", 20)).place(x=320, y=10)
Label(root, text="ІО-13", font=("Arial", 20)).place(x=393, y=50)
Label(root, text="Номер у списку групи: 9", font=("Arial", 20)).place(x=290, y=85)
Label(root, text=f"Номер варіанту: {option}", font=("Arial", 20)).place(x=325, y=120)
Label(root, text="Алгоритм Левіта", font=("Arial", 20)).place(x=55, y=170)
Button(root, text="Показати граф", command=create_graph, font=("Arial", 18)).place(x=70, y=240)
e1 = Entry(root, font=("Arial", 15))
e1.place(x=30, y=350, height=30, width=100)
e2 = Entry(root, font=("Arial", 15))
e2.place(x=180, y=350, height=30, width=100)
Label(text="Від", font=("Arial", 12)).place(x=65, y=320)
Label(text="До", font=("Arial", 12)).place(x=220, y=320)
Button(root, text="Найкоротший шлях", command=lambda: find_shortest_way(e1.get(), e2.get()),
       font=("Arial", 18)).place(x=40, y=440)

root.mainloop()

