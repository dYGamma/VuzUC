import networkx as nx
import matplotlib.pyplot as plt

# Создаем пустой граф
G = nx.DiGraph()

# Добавляем задачи и их зависимости
tasks = [
    ("I", "A", {"weight": 2}),
    ("I", "E", {"weight": 1}),
    ("A", "H", {"weight": 1}),
    ("A", "E", {"weight": 3}),
    ("H", "B", {"weight": 5}),
    ("H", "M", {"weight": 0}),
    ("E", "M", {"weight": 4}),
    ("B", "K", {"weight": 2}),
    ("M", "K", {"weight": 2}),
    ("K", "C", {"weight": 3})
]

# Добавляем задачи и ребра в граф
G.add_edges_from(tasks)

# Присваиваем номера и буквенные обозначения вершинам
node_labels = {node: f"{i+1}. {node}" for i, node in enumerate(G.nodes)}

# Раскрасим вершины в зависимости от критического пути
critical_path = nx.dag_longest_path(G)
node_colors = ["red" if node in critical_path else "blue" for node in G.nodes]

# Рисуем граф
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, node_size=1500, font_size=12, font_weight="bold")
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black")

# Показываем граф
plt.title("Сетевой график с нумерацией и буквенными обозначениями вершин")
plt.show()
