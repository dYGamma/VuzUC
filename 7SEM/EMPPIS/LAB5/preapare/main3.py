import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import minimize

# Функция Эасома для трех переменных
def fEaso(x):
    result = -np.cos(x[0]) * np.cos(x[1]) * np.cos(x[2]) * np.exp(-((x[0] - np.pi) ** 2 + (x[1] - np.pi) ** 2 + (x[2] - np.pi) ** 2))
    return result

# Параметры эволюционной стратегии
population_size = 300  # Размер популяции
max_generations = 300  # Лимит поколений
mutation_probability = 0.5  # Начальная вероятность мутации
initial_mutation_sigma = 0.5  # Начальное стандартное отклонение для мутации

# Инициализация популяции
initial_population = np.random.uniform(-np.pi, np.pi, (population_size, 3))

# Начало замера времени
start_time = time.time()

best_fitness_history = []
best_solution = initial_population[0]
best_fitness = fEaso(best_solution)

mutation_sigma = initial_mutation_sigma

# Основной цикл
dynamic_mutation_factor = 0.1  # Фактор для изменения вероятности мутации
for generation in range(max_generations):
    # Оценка популяции
    fitness_values = np.array([fEaso(ind) for ind in initial_population])

    # Поиск лучшего решения
    current_best_fitness = np.min(fitness_values)
    best_idx = np.argmin(fitness_values)

    if current_best_fitness < best_fitness:
        best_fitness = current_best_fitness
        best_solution = initial_population[best_idx]

    best_fitness_history.append(best_fitness)

    # Создание новой популяции
    new_population = []
    sorted_indices = np.argsort(fitness_values)
    selected_parents = initial_population[sorted_indices[:population_size // 5]]  # Выбор лучших 20%

    for _ in range(population_size):
        parent = selected_parents[np.random.choice(selected_parents.shape[0])]

        # Мутация
        if np.random.rand() < mutation_probability:
            mutation_sigma *= np.random.uniform(0.95, 1.05)  # Динамическое изменение sigma
            child = parent + np.random.normal(0, mutation_sigma, 3)
            child = np.clip(child, -np.pi, np.pi)  # Ограничение области поиска
        else:
            child = parent

        new_population.append(child)

    initial_population = np.array(new_population)

    # Динамическое изменение вероятности мутации
    mutation_probability = max(0.1, mutation_probability - dynamic_mutation_factor / max_generations)

# Локальная оптимизация для уточнения результата
result = minimize(fEaso, best_solution, bounds=[(-np.pi, np.pi)] * 3)
if result.success and result.fun < best_fitness:
    best_fitness = result.fun
    best_solution = result.x

# Визуализация сходимости
plt.figure(figsize=(10, 6))
plt.plot(best_fitness_history, label="Лучшее значение функции")
plt.axhline(y=-1, color='r', linestyle='--', label="Известный оптимум (-1)")
plt.xlabel("Поколение")
plt.ylabel("Лучшее значение функции")
plt.title("Сходимость эволюционной стратегии")
plt.legend()
plt.grid()
plt.show()

# Результаты
print(f'Лучшее найденное решение: x1 = {best_solution[0]:.6f}, x2 = {best_solution[1]:.6f}, x3 = {best_solution[2]:.6f}')
print(f'Значение функции в этой точке: {best_fitness:.6f}')
print(f'Известный оптимум: f(x1,x2,x3) = -1')
print(f'Время выполнения программы: {time.time() - start_time:.2f} секунд')
