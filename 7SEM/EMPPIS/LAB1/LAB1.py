import numpy as np
import matplotlib.pyplot as plt

# Задаем функцию для нахождения минимума
def func(x):
    # Избегаем деления на ноль
    x = np.where(x == 0, 1e-8, x)
    return np.cos(x - 0.5) / np.abs(x)

# Генетический алгоритм
def genetic_algorithm(func, bounds, population_size, generations, crossover_rate, mutation_rate):
    # Инициализация начальной популяции
    population = np.random.uniform(bounds[0], bounds[1], population_size)
    fitness = func(population)

    best_individuals = []
    best_fitness_history = []

    for generation in range(generations):
        # Оценка пригодности
        fitness = func(population)

        # Сохраняем лучший результат
        best_index = np.argmin(fitness)
        best_individual = population[best_index]
        best_individuals.append(best_individual)
        best_fitness_history.append(fitness[best_index])

        # Селекция с использованием метода турнира
        selected_population = []
        for _ in range(population_size):
            i, j = np.random.randint(0, population_size, 2)
            if fitness[i] < fitness[j]:
                selected_population.append(population[i])
            else:
                selected_population.append(population[j])
        selected_population = np.array(selected_population)

        # Кроссинговер с использованием одноточечного метода
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[(i+1) % population_size]
            if np.random.rand() < crossover_rate:
                alpha = np.random.rand()
                child1 = alpha * parent1 + (1 - alpha) * parent2
                child2 = (1 - alpha) * parent1 + alpha * parent2
            else:
                child1, child2 = parent1, parent2
            new_population.extend([child1, child2])

        # Мутация с использованием нормального распределения
        new_population = np.array(new_population)
        mutation_array = np.random.rand(population_size) < mutation_rate
        mutation_values = np.random.normal(0, 1, population_size)
        new_population[mutation_array] += mutation_values[mutation_array]

        # Ограничение значений в пределах bounds
        population = np.clip(new_population, bounds[0], bounds[1])

    return best_individuals, best_fitness_history

# Основные параметры алгоритма
population_size = 200
generations = 100
crossover_rate = 0.8
mutation_rate = 0.1
bounds = [-10, -1e-8]  # Избегаем нуля

# Запуск генетического алгоритма
best_individuals, best_fitness_history = genetic_algorithm(func, bounds, population_size, generations, crossover_rate, mutation_rate)

# Вывод графика функции и найденного минимума
x = np.linspace(bounds[0], -1e-8, 1000)
y = func(x)

plt.figure(figsize=(12, 5))

# График эволюции решения
plt.subplot(1, 2, 1)
plt.plot(x, y, label='cos(x-0.5)/|x|')
plt.scatter(best_individuals, func(np.array(best_individuals)), color='red', s=10, label='Найденный минимум')
plt.title('Эволюция генетического алгоритма')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)

# График изменения наилучшего результата по поколениям
plt.subplot(1, 2, 2)
plt.plot(best_fitness_history, label='Лучший фитнес на поколении')
plt.title('История улучшений фитнес-функции')
plt.xlabel('Поколение')
plt.ylabel('Значение фитнес-функции')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Вывод найденного минимума
best_x = best_individuals[np.argmin(best_fitness_history)]
best_f = func(best_x)
print(f"Найденное решение: x = {best_x}, f(x) = {best_f}")
