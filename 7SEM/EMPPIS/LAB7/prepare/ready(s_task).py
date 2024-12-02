import numpy as np
import matplotlib.pyplot as plt
import time
from tabulate import tabulate

# Параметры PSO
population_size = 500          # Количество частиц
max_iterations = 500           # Максимальное количество итераций
w = 0.5                         # Коэффициент инерции
c1 = 1.5                        # Коэффициент когнитивной компоненты (личный опыт)
c2 = 1.5                        # Коэффициент социальной компоненты (опыт группы)
x_min, x_max = 0, 2 * np.pi     # Диапазон для переменных

# Функция Эасома для n-мерного случая
def fEaso(x):
    return -np.prod(np.cos(x)) * np.exp(-np.sum((x - np.pi) ** 2))

# Добавление функции для улучшения инициализации частиц
def initialize_particles(n):
    return np.random.uniform(x_min, x_max, (population_size, n))

def run_pso(n):
    # Инициализация частиц и их скоростей
    particles = initialize_particles(n)
    velocities = np.random.uniform(-1, 1, (population_size, n))

    # Инициализация лучших позиций
    personal_best_positions = np.copy(particles)
    personal_best_scores = np.array([fEaso(p) for p in particles])
    global_best_position = particles[np.argmin(personal_best_scores)]
    global_best_score = np.min(personal_best_scores)

    start_time = time.time()

    # Основной цикл PSO
    for iteration in range(max_iterations):
        for i in range(population_size):
            cognitive_component = c1 * np.random.rand() * (personal_best_positions[i] - particles[i])
            social_component = c2 * np.random.rand() * (global_best_position - particles[i])
            velocities[i] = w * velocities[i] + cognitive_component + social_component
            particles[i] += velocities[i]
            particles[i] = np.clip(particles[i], x_min, x_max)

            fitness = fEaso(particles[i])
            if fitness < personal_best_scores[i]:
                personal_best_scores[i] = fitness
                personal_best_positions[i] = particles[i]

        current_best_index = np.argmin(personal_best_scores)
        if personal_best_scores[current_best_index] < global_best_score:
            global_best_score = personal_best_scores[current_best_index]
            global_best_position = personal_best_positions[current_best_index]

    execution_time = time.time() - start_time

    print("\n\033[1mРезультаты для n = {}:\033[0m".format(n))
    print("\033[94m\033[1mЛучшее найденное решение:\033[0m", global_best_position)
    print("\033[94m\033[1mЗначение функции в этой точке:\033[0m", f"{global_best_score:.6f}")
    print("\033[94m\033[1mВремя выполнения:\033[0m", f"{execution_time:.4f} секунд\n")

    return global_best_position, global_best_score, execution_time

# Запуск для различных значений n
results = {}
for n in [2, 4, 6, 10]:
    results[n] = run_pso(n)

# Табличный вывод результатов
headers = ["Размерность n", "Лучшее решение", "Значение функции", "Время выполнения (сек)"]
table_data = [
    [n, np.array2string(results[n][0], precision=4, separator=','), f"{results[n][1]:.6f}", f"{results[n][2]:.4f}"]
    for n in results
]
print("\033[1m\nСводная таблица результатов:\033[0m")
print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Визуализация времени выполнения
dims = list(results.keys())
times = [results[n][2] for n in dims]
plt.figure(figsize=(8, 5))
plt.bar(dims, times, color='skyblue')
plt.xlabel('Размерность n', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.title('Время выполнения алгоритма PSO для различных размерностей', fontsize=14)
plt.xticks(dims)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
