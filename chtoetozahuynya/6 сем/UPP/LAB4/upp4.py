import networkx as nx
import pandas as pd

class Node:
    def __init__(self, name):
        self.name = name
        self.incoming_edges = []
        self.outgoing_edges = []
        self.early_start = 0
        self.early_finish = 0
        self.late_start = 0
        self.late_finish = 0
        self.duration = 0

class Edge:
    def __init__(self, source, target, duration):
        self.source = source
        self.target = target
        self.duration = duration

def calculate_early_times(node, current_time):
    if node.early_start < current_time:
        node.early_start = current_time
    node.early_finish = node.early_start + node.duration
    for edge in node.outgoing_edges:
        calculate_early_times(edge.target, node.early_finish)

def calculate_late_times(node, current_time):
    if node.late_finish == 0 or node.late_finish > current_time:
        node.late_finish = current_time
    node.late_start = node.late_finish - node.duration
    for edge in node.incoming_edges:
        calculate_late_times(edge.source, node.late_start - edge.duration)

def print_network(nodes):
    print("Node\tEarly Start\tEarly Finish\tLate Start\tLate Finish")
    for node in nodes:
        print(f"{node.name}\t{node.early_start}\t\t{node.early_finish}\t\t{node.late_start}\t\t{node.late_finish}")

def main():
    edges = [
        ("I", "A", 2),
        ("I", "E", 1),
        ("A", "H", 1),
        ("A", "E", 3),
        ("H", "B", 5),
        ("H", "M", 0),
        ("E", "M", 4),
        ("B", "K", 2),
        ("M", "K", 2),
        ("K", "C", 3)
    ]

    nodes = {}
    for edge in edges:
        source_name, target_name, duration = edge
        if source_name not in nodes:
            nodes[source_name] = Node(source_name)
        if target_name not in nodes:
            nodes[target_name] = Node(target_name)
        source_node = nodes[source_name]
        target_node = nodes[target_name]
        new_edge = Edge(source_node, target_node, duration)
        source_node.outgoing_edges.append(new_edge)
        target_node.incoming_edges.append(new_edge)
        source_node.duration = max(source_node.duration, duration)

    start_node = nodes["I"]
    calculate_early_times(start_node, 0)

    # Шаги алгоритма табличного метода
    for node in nodes.values():
        if not node.incoming_edges:
            node.late_finish = node.early_finish
            node.late_start = node.early_start
    for node in reversed(list(nodes.values())):
        if node == start_node:
            continue
        if not node.outgoing_edges:
            node.late_finish = max([n.late_finish for n in nodes.values()])
            node.late_start = node.late_finish - node.duration
        else:
            node.late_finish = min([n.late_finish for n in nodes.values() if node.name in [e.source.name for e in n.outgoing_edges]])
            node.late_start = node.late_finish - node.duration

    # Вывод табличного представления
    print_network(nodes.values())

if __name__ == "__main__":
    main()
