import pulp

# Создаем задачу для максимизации прибыли
model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Определяем переменные (целочисленные переменные x1, x2, x3, x4, x5)
x1 = pulp.LpVariable('x1', lowBound=0, cat='Integer')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Integer')
x3 = pulp.LpVariable('x3', lowBound=0, cat='Integer')
x4 = pulp.LpVariable('x4', lowBound=0, cat='Integer')
x5 = pulp.LpVariable('x5', lowBound=0, cat='Integer')

# Целевая функция: максимизация прибыли
model += 40 * x1 + 70 * x2 + 120 * x3 + 120 * x4 + 50 * x5, "Profit"

# Ограничения по ресурсам
model += 2 * x1 + 3 * x2 + 5 * x3 + 4 * x4 + 4 * x5 <= 900  # Трудозатраты
model += 2 * x1 + 2 * x2 + 4 * x3 + 5 * x4 + 0 * x5 <= 8500  # Металл
model += 1 * x1 + 3 * x2 + 2 * x3 + 0 * x4 + 4 * x5 <= 4000  # Пластик
model += 1 * x1 + 2 * x2 + 3 * x3 + 3 * x4 + 2 * x5 <= 5000  # Краска

# Решение задачи
model.solve()

# Вывод результатов
print(f"Оптимальное количество холодильников марки 1: {x1.varValue}")
print(f"Оптимальное количество холодильников марки 2: {x2.varValue}")
print(f"Оптимальное количество холодильников марки 3: {x3.varValue}")
print(f"Оптимальное количество холодильников марки 4: {x4.varValue}")
print(f"Оптимальное количество холодильников марки 5: {x5.varValue}")
print(f"Максимальная прибыль: {pulp.value(model.objective)}")
