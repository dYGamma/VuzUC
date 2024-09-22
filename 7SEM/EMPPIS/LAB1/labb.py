import numpy as np
import matplotlib.pyplot as plt
import random

# Определяем целевую функцию
def fitness(x):
    return np.cos(x - 0.5) / abs(x) if x != 0 else 0  # Избегаем деления на 0

# Генерация начальной популяции
def generate_population(size, x_bounds):
    return [random.uniform(*x_bounds) for _ in range(size)]

# Выбор родителей
def select_parents(population):
    weights = [fitness(x) for x in population]
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]
    return np.random.choice(population, size=2, p=probabilities)

# Кроссинговер
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

# Мутация
def mutate(x, mutation_rate):
    if random.random() < mutation_rate:
        return x + random.uniform(-1, 1)  # Случайное изменение
    return x

# Основной генетический алгоритм
def genetic_algorithm(pop_size, x_bounds, generations, crossover_rate, mutation_rate):
    population = generate_population(pop_size, x_bounds)
    best_solutions = []

    for generation in range(generations):
        new_population = []
        for _ in range(pop_size // 2):  # Формируем новую популяцию
            parent1, parent2 = select_parents(population)
            if random.random() < crossover_rate:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
            else:
                child1, child2 = parent1, parent2
            
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))

        population = new_population
        best_solution = max(population, key=fitness)
        best_solutions.append(fitness(best_solution))
        print(f'Generation {generation}: Best solution = {best_solution}, Fitness = {fitness(best_solution)}')

    return best_solutions, best_solution

# Параметры алгоритма
pop_size = 50
x_bounds = (-10, 10)
generations = 100
crossover_rate = 0.7
mutation_rate = 0.1

# Запуск алгоритма
best_solutions, best_solution = genetic_algorithm(pop_size, x_bounds, generations, crossover_rate, mutation_rate)

# Построение графика функции
x_values = np.linspace(-10, 10, 400)
y_values = [fitness(x) for x in x_values]
plt.plot(x_values, y_values, label='Fitness Function')
plt.scatter([best_solution], [fitness(best_solution)], color='red', label='Best Solution', zorder=5)

# Отображение найденного экстремума для каждого поколения
plt.title('Genetic Algorithm Optimization')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()
plt.show()

# Сравнение с действительным решением
actual_max = max(x_values, key=fitness)
print(f'Actual max solution = {actual_max}, Fitness = {fitness(actual_max)}')
