import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import minimize_scalar
# близко к 0 Однако, из-за особенности функции значение функции для x = 0 будет бесконечность
# Целевая функция
def target_function(x):
    if x == 0:
        return float('-inf')  # Выколотая точка в отрезке, заданном условием
    return np.cos(x - 0.5) / abs(x)

# Генерация начальной популяции
def generate_population(pop_size, x_min, x_max):
    return [random.uniform(x_min, x_max) for i in range(pop_size)]

# Оценка приспособленности особей
def fitness(population):
    return [target_function(x) for x in population]

# Выбор родителей
def select_parents(population, fitness_values):
    parents = []
    for k in range(len(population)):
        i, j = random.sample(range(len(population)), 2)
        if fitness_values[i] > fitness_values[j]:
            parents.append(population[i])
        else:
            parents.append(population[j])
    return parents

# Кроссинговер
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

# Мутация
def mutate(population, mutation_rate, x_min, x_max):
    for i in range(len(population)):
        if random.random() < mutation_rate:
            population[i] = random.uniform(x_min, x_max)
    return population

# Построение графика
def plot_generation(population, generation, x_min, x_max, best_values, count):
    x = np.linspace(x_min, x_max, 1000 * count)
    y = [target_function(val) for val in x]

    plt.figure()
    plt.plot(x, y, label='f(x) = cos(x-0.5) / |x|')
    plt.scatter(population, [target_function(ind) for ind in population], color='red', label='Population')

    plt.title(f'График функции и популяции на поколении {generation}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # Инициализация переменных
    population_size = 50  # Размер популяции
    p_crossover = 0.5  # Вероятность появления потомка
    p_mutation = 0.01  # Вероятность мутации у потомка
    x_min = -10
    x_max = 10
    population = generate_population(population_size, x_min, x_max)  # Начальная популяция
    generation = 0  # Номер поколения
    max_generations = 50  # Лимит по числу поколений
    best_fitness = float('-inf')  # Текущая лучшая особь
    best_values = []  # Массив лучших особей
    plot_steps = [0, 10, 25, 40]  # Номера популяций для которых будут строиться графики
    count = 1  # Вспомогательный счетчик для построения графика

    while generation < max_generations:
        fitness_values = fitness(population)
        best_idx = np.argmax(fitness_values)
        best_value = population[best_idx]
        best_values.append(best_value)

        # Оценка улучшения
        if fitness_values[best_idx] > best_fitness:
            best_fitness = fitness_values[best_idx]

        # Построение графика текущего поколения
        plt.ion()
        if generation in plot_steps:
            plot_generation(population, generation, x_min, x_max, best_values, count)
            plt.draw()
            plt.pause(5)
            plt.close()
            count += 100
        plt.ioff()

        # Селекция родителей
        parents = select_parents(population, fitness_values)

        # Создание новой популяции через кроссинговер
        new_population = []
        for i in range(0, population_size, 2):
            parent1, parent2 = random.sample(parents, 2)
            if random.random() < p_crossover:
                offspring1 = crossover(parent1, parent2)
                offspring2 = crossover(parent2, parent1)
            else:
                offspring1, offspring2 = parent1, parent2
            new_population.extend([offspring1, offspring2])

        # Мутация
        population = mutate(new_population, p_mutation, x_min, x_max)
        generation += 1

    # Построение графика для последнего поколения
    plot_generation(population, generation, x_min, x_max, best_values, count)

    # Вывод результата генетического алгоритма
    print(f"Population size = {population_size}, P crossover = {p_crossover}, P mutation = {p_mutation}")
    print(f"Maximum found at x = {best_values[-1]}, at generation = {generation}")

    # Решение с помощью SciPy
    result = minimize_scalar(lambda x: -target_function(x), bounds=(x_min, x_max), method='bounded')

    # # Вывод решения SciPy
    # print("\nScipy Optimization:")
    # print(f"Maximum found at x = {result.x}, f(x) = {target_function(result.x)}")
