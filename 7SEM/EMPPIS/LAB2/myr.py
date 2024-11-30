import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import time

# Определение функции sin(2x)/x^2
def target_function(x):
    return (np.sin(2 * x[0]) / (x[0] ** 2)),

# Параметры алгоритма
population_size = 170
num_generations = 25
mutation_rate = 0.1
crossover_rate = 0.8
elitism_rate = 0.1
max_no_improve_generations = 20

# Инициализация популяции в пределах [-20, -3.1]
def initialize_population(size, dimensions, lower_bound=-20, upper_bound=-3.1):
    return np.random.uniform(lower_bound, upper_bound, (size, dimensions))

# Селекция с использованием рулетки
def roulette_wheel_selection(population, fitness_values):
    min_fitness = np.min(fitness_values)
    shifted_fitness = fitness_values - min_fitness + 1e-6
    selection_probs = shifted_fitness / np.sum(shifted_fitness)
    return population[np.random.choice(len(population), p=selection_probs)]

# Плоский кроссовер
def flat_crossover(parent1, parent2):
    return np.random.uniform(parent1, parent2)

# Линейный кроссовер
def linear_crossover(parent1, parent2):
    offspring1 = 0.5 * parent1 + 0.5 * parent2
    offspring2 = 1.5 * parent1 - 0.5 * parent2
    return offspring1, offspring2

# Смешанный BLX-alpha кроссовер с уменьшенным alpha
def blx_alpha_crossover(parent1, parent2, alpha=0.2):
    cmin = np.minimum(parent1, parent2)
    cmax = np.maximum(parent1, parent2)
    I = cmax - cmin
    return np.random.uniform(cmin - I * alpha, cmax + I * alpha)

# Оператор мутации
def mutate(individual, mutation_rate=0.1, lower_bound=-20, upper_bound=-3.1, generation=None, max_generations=None):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            if generation is not None and max_generations is not None:
                b = 3
                r = np.random.rand()
                delta = (1 - (generation / max_generations)) ** b * r * (upper_bound - lower_bound)
                direction = random.choice([-1, 1])
                individual[i] += direction * delta
            else:
                individual[i] = np.random.uniform(lower_bound, upper_bound)
        individual[i] = np.clip(individual[i], lower_bound, upper_bound)
    return individual

# Генетический алгоритм с различными типами кроссовера и подробным выводом
def genetic_algorithm(dimensions=1):
    population = initialize_population(population_size, dimensions)
    best_solutions = []
    best_fitness_values = []
    avg_fitness_values = []
    diversity_over_time = []
    best_fitness = float('inf')
    no_improve_count = 0
    crossover_usage = {"flat": 0, "linear": 0, "blx_alpha": 0}
    mutation_count = 0

    start_time = time.time()

    for generation in range(num_generations):
        fitness_values = np.array([target_function(ind)[0] for ind in population])

        # Запись лучших значений функции приспособленности
        best_index = np.argmin(fitness_values)
        current_best_fitness = fitness_values[best_index]
        best_solutions.append(population[best_index])
        best_fitness_values.append(current_best_fitness)

        # Вычисление среднего и максимального значения приспособленности
        avg_fitness = np.mean(fitness_values)
        avg_fitness_values.append(avg_fitness)
        max_fitness = np.max(fitness_values)

        # Проверка на отсутствие улучшения
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            no_improve_count = 0
        else:
            no_improve_count += 1

        if no_improve_count >= max_no_improve_generations:
            print(f"Остановка: отсутствие улучшения в течение {max_no_improve_generations} поколений.")
            break

        # Сохранение лучших особей (элитизм)
        num_elites = int(elitism_rate * population_size)
        elite_individuals = population[np.argsort(fitness_values)[:num_elites]]

        new_population = []
        while len(new_population) < (population_size - num_elites):
            parent1 = roulette_wheel_selection(population, fitness_values)
            parent2 = roulette_wheel_selection(population, fitness_values)

            if np.random.rand() < crossover_rate:
                crossover_choice = np.random.choice(['flat', 'linear', 'blx_alpha'])
                if crossover_choice == 'flat':
                    offspring1 = flat_crossover(parent1, parent2)
                    offspring2 = flat_crossover(parent1, parent2)
                    crossover_usage['flat'] += 1
                elif crossover_choice == 'linear':
                    offspring1, offspring2 = linear_crossover(parent1, parent2)
                    crossover_usage['linear'] += 1
                elif crossover_choice == 'blx_alpha':
                    offspring1 = blx_alpha_crossover(parent1, parent2)
                    offspring2 = blx_alpha_crossover(parent1, parent2)
                    crossover_usage['blx_alpha'] += 1
            else:
                offspring1, offspring2 = parent1, parent2

            new_population.append(mutate(offspring1, mutation_rate, generation=generation, max_generations=num_generations))
            new_population.append(mutate(offspring2, mutation_rate, generation=generation, max_generations=num_generations))
            mutation_count += 2

        new_population.extend(elite_individuals)
        population = np.array(new_population[:population_size])

        diversity = np.mean(np.std(population, axis=0))
        diversity_over_time.append(diversity)

        # Печать подробной информации о поколении
        print(f"Поколение {generation + 1}:")
        print(f"  Минимальная приспособленность: {current_best_fitness:.6f}")
        print(f"  Средняя приспособленность: {avg_fitness:.6f}")
        print(f"  Максимальная приспособленность: {max_fitness:.6f}")
        print(f"  Разнообразие популяции: {diversity:.6f}")

    elapsed_time = time.time() - start_time

    # Печать итогов генетического алгоритма
    print("\n=============== Результаты Генетического Алгоритма ===============")
    print(f"Время выполнения: {elapsed_time:.2f} секунд")
    print(f"Лучшее значение функции приспособленности: {best_fitness:.6f}")
    print(f"Параметры алгоритма: Размер популяции = {population_size}, Число поколений = {num_generations}, Вероятность мутации = {mutation_rate}, Вероятность кроссовера = {crossover_rate}, Уровень элитизма = {elitism_rate}")
    print("Использование операторов кроссовера:")
    for crossover, count in crossover_usage.items():
        print(f"  {crossover}: {count} раз(а)")
    print(f"Количество примененных мутаций: {mutation_count}")
    print("==================================================================\n")

    return best_solutions, best_fitness_values, avg_fitness_values, diversity_over_time

# Запуск генетического алгоритма для n=2 и n=3 и вывод результата
print("========= Запуск генетического алгоритма для n=2 =========")
best_solutions_n2, best_fitness_values_n2, avg_fitness_values_n2, diversity_over_time_n2 = genetic_algorithm(dimensions=2)

print("========= Запуск генетического алгоритма для n=3 =========")
best_solutions_n3, best_fitness_values_n3, avg_fitness_values_n3, diversity_over_time_n3 = genetic_algorithm(dimensions=3)

# Построение 3D-графика функции и точек популяции для n=2 с улучшенным углом обзора
x = np.linspace(-20, -3.1, 100)
y = np.linspace(-20, -3.1, 100)
x, y = np.meshgrid(x, y)
z = np.array([[target_function([x[i, j]])[0] for j in range(100)] for i in range(100)])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.6)

# Отображение точек популяции для n=2
population_points = np.array(best_solutions_n2)
ax.scatter(population_points[:, 0], population_points[:, 0], [target_function(ind)[0] for ind in population_points], color='r')

ax.view_init(elev=45, azim=45)  # Увеличение угла обзора
ax.set_xlabel('x1', fontsize=12, labelpad=10)
ax.set_ylabel('x2', fontsize=12, labelpad=10)
ax.set_zlabel('f(x)', fontsize=12, labelpad=10)
plt.title('График функции sin(2x)/x^2 и точки популяции (n=2)')
plt.show()

# Построение графика лучших значений функции приспособленности для n=2 и n=3
plt.figure(figsize=(10, 5))
plt.plot(range(len(best_fitness_values_n2)), best_fitness_values_n2, label='Лучшее значение n=2', color='blue')
plt.plot(range(len(best_fitness_values_n3)), best_fitness_values_n3, label='Лучшее значение n=3', color='orange')
plt.xlabel('Поколение')
plt.ylabel('Значение приспособленности')
plt.title('Эволюция лучшего значения функции приспособленности для n=2 и n=3')
plt.legend()
plt.grid(True)
plt.show()

# Построение графика среднего значения функции приспособленности для n=2 и n=3
plt.figure(figsize=(10, 5))
plt.plot(range(len(avg_fitness_values_n2)), avg_fitness_values_n2, linestyle='--', label='Среднее значение n=2', color='red')
plt.plot(range(len(avg_fitness_values_n3)), avg_fitness_values_n3, linestyle='--', label='Среднее значение n=3', color='green')
plt.xlabel('Поколение')
plt.ylabel('Значение приспособленности')
plt.title('Эволюция среднего значения функции приспособленности для n=2 и n=3')
plt.legend()
plt.grid(True)
plt.show()

# Построение графика разнообразия популяции для n=2 и n=3 с добавлением горизонтальных пороговых линий
plt.figure(figsize=(10, 5))
plt.plot(range(len(diversity_over_time_n2)), diversity_over_time_n2, label='Разнообразие n=2')
plt.plot(range(len(diversity_over_time_n3)), diversity_over_time_n3, label='Разнообразие n=3', color='orange')
plt.axhline(y=2.5, color='r', linestyle='--', label='Порог разнообразия')  # Добавление пороговой линии
plt.xlabel('Поколение')
plt.ylabel('Разнообразие популяции')
plt.title('Разнообразие популяции для n=2 и n=3 с порогами')
plt.legend()
plt.grid(True)
plt.show()