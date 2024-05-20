import pulp

# Данные
demand = [100, 150, 200, 120, 180]
costs = [
    [5, 7, 8, 6, 9],
    [8, 6, 7, 5, 9],
    [6, 9, 5, 8, 7],
    [7, 8, 6, 9, 5],
    [9, 5, 7, 6, 8]
]

# Создание переменных
x = pulp.LpVariable.dicts("shipment", ((i, j) for i in range(1, 6) for j in range(1, 6)), lowBound=0, cat='Integer')

# Создание задачи
prob = pulp.LpProblem("Warehouse_Location", pulp.LpMinimize)

# Целевая функция
prob += pulp.lpSum([x[i, j] * costs[i-1][j-1] for i in range(1, 6) for j in range(1, 6)])

# Ограничения на спрос
for j in range(1, 6):
    prob += pulp.lpSum([x[i, j] for i in range(1, 6)]) == demand[j-1]

# Решение задачи
prob.solve()

# Вывод результатов
print("Результат:")
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Общие затраты:", pulp.value(prob.objective))
