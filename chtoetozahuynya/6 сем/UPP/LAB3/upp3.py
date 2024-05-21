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

# Расчет временных параметров матричным методом
def calculate_parameters(adjacency_matrix):
    num_tasks = len(adjacency_matrix)
    ES = np.zeros(num_tasks)  # Ранние сроки начала выполнения задач
    EF = np.zeros(num_tasks)  # Ранние сроки окончания выполнения задач
    LS = np.zeros(num_tasks)  # Поздние сроки начала выполнения задач
    LF = np.zeros(num_tasks)  # Поздние сроки окончания выполнения задач
    EET = np.zeros(num_tasks)  # Ранние времена наступления событий
    LET = np.zeros(num_tasks)  # Поздние времена наступления событий
    TF = np.zeros(num_tasks)  # Полные резервы времени выполнения работы
    FF = np.zeros(num_tasks)  # Свободные резервы времени выполнения работы
    IF = np.zeros(num_tasks)  # Независимые резервы времени выполнения работы
    ti = np.array([e[2]['weight'] for e in G.edges(data=True)])  # Продолжительности работ

    # Рассчитываем ранние сроки начала и окончания
    for i in range(num_tasks):
        if np.all(adjacency_matrix[:, i] == 0):  # Если задача не имеет предшественников
            ES[i] = 0
            EF[i] = ES[i] + np.max(adjacency_matrix[i, :])
        else:
            ES[i] = np.max(EF[list(np.where(adjacency_matrix[:, i] > 0)[0])])
            EF[i] = ES[i] + ti[i]

    # Рассчитываем поздние сроки начала и окончания
    LS[num_tasks - 1] = LF[num_tasks - 1] = EF[num_tasks - 1]
    for i in range(num_tasks - 2, -1, -1):
        if np.any(adjacency_matrix[i, :] > 0):  # Если у задачи есть последователи
            LF[i] = np.min(LS[list(np.where(adjacency_matrix[i, :] > 0)[0])])
            LS[i] = LF[i] - ti[i]

    # Рассчитываем ранние и поздние времена наступления событий
    for i in range(num_tasks):
        EET[i] = EF[i]
        LET[i] = LS[i]

    # Рассчитываем полные резервы времени выполнения работы
    for i in range(num_tasks):
        if np.any(adjacency_matrix[i, :] > 0):  # Если у задачи есть последователи
            TF[i] = LET[np.where(adjacency_matrix[i, :] > 0)[0][0]] - EET[i] - ti[i]

    # Рассчитываем свободные резервы времени выполнения работы
    for i in range(num_tasks):
        if np.any(adjacency_matrix[i, :] > 0):  # Если у задачи есть последователи
            FF[i] = EET[np.where(adjacency_matrix[i, :] > 0)[0][0]] - ES[i] - ti[i]

    # Рассчитываем независимые резервы времени выполнения работы
    for i in range(num_tasks):
        if np.any(adjacency_matrix[i, :] > 0):  # Если у задачи есть последователи
            IF[i] = EET[np.where(adjacency_matrix[i, :] > 0)[0][0]] - LET[i] - ti[i]
    
    # Рассчитываем продолжительность критического пути
    critical_path_duration = LF[-1] - EF[0]

    # Рассчитываем резерв времени наступления события
    event_reserve = LET - EET

    return ES, EF, LS, LF, EET, LET, TF, FF, IF, critical_path_duration, event_reserve

# Выполним расчет временных параметров
ES, EF, LS, LF, EET, LET, TF, FF, IF, critical_path_duration, event_reserve = calculate_parameters(adjacency_matrix)

# Выведем результаты
print("Продолжительности работ (ti):", [e[2]['weight'] for e in G.edges(data=True)])
print("Ранние сроки начала (ES):", ES)
print("Ранние сроки окончания (EF):", EF)
print("Поздние сроки начала (LS):", LS)
print("Поздние сроки окончания (LF):", LF)
print("Ранние времена наступления событий (EET):", EET)
print("Поздние времена наступления событий (LET):", LET)
print("Полные резервы времени выполнения работы (TF):", TF)
print("Свободные резервы времени выполнения работы (FF):", FF)
print("Независимые резервы времени выполнения работы (IF):", IF)
print("Продолжительность критического пути:", critical_path_duration)
print("Резерв времени наступления события:", event_reserve)
