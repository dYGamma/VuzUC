import numpy as np
import networkx as nx

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

# Получаем матрицу смежности
adjacency_matrix = nx.adjacency_matrix(G).todense()

# Выводим матрицу смежности
print("Матрица смежности сетевого графика:")
print(adjacency_matrix)
