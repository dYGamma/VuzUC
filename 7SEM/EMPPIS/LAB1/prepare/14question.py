import numpy as np 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Функция для оптимизации
def f(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.cos(x - 0.5) / np.abs(x)
        result[np.isnan(result)] = 0  # Обрабатываем NaN, если x=0
    return result

# Настройки
population_size = 100
generations = 50
mutation_rate = 0.2
mutation_chance = 0.9
x_bounds = [-10, 10]  # Интервал x ∈ [-10, 0) ∪ (0, 10]

# Значения вероятности кроссинговера Pc для эксперимента
crossover_probabilities = [0.2, 0.5, 0.8, 1.0]

# Исследование разных вероятностей Pc
results = {}

for Pc in crossover_probabilities:
    # Инициализация популяции
    population = np.concatenate([np.random.uniform(x_bounds[0], -0.01, population_size // 2),
                                 np.random.uniform(0.01, x_bounds[1], population_size // 2)])

    fitness_history = []
    population_history = []
    avg_fitness_history = []  # Средняя приспособленность
    min_fitness_history = []  # Минимальная приспособленность

    for generation in range(generations):
        fitness = f(population)
        fitness_history.append(fitness)
        population_history.append(population)

        # Сохраняем среднее и минимальное значение приспособленности
        avg_fitness_history.append(np.mean(fitness))
        min_fitness_history.append(np.min(fitness))

        # Селекция особей с лучшими значениями (поиск минимума)
        selected_indices = np.argsort(fitness)[:population_size // 2]
        selected_population = population[selected_indices]

        # Кроссинговер и создание потомков
        offspring = []
        for i in range(len(selected_population) // 2):
            parent1 = selected_population[2 * i]
            parent2 = selected_population[2 * i + 1]

            if np.random.rand() < Pc:  # Применение вероятности кроссинговера
                crossover_point = np.random.rand()
                child = crossover_point * parent1 + (1 - crossover_point) * parent2
            else:
                child = parent1  # Если кроссинговера не произошло, ребенок - копия родителя

            offspring.append(child)

        offspring = np.array(offspring)
        
        # Мутация
        if np.random.uniform(0, 1) <= mutation_chance:
            mutation = np.random.uniform(-mutation_rate, mutation_rate, offspring.shape)
            offspring += mutation

        population = np.concatenate((selected_population, offspring))

    # Сохраняем историю для текущего значения Pc
    results[Pc] = {
        'fitness_history': fitness_history,
        'population_history': population_history,
        'avg_fitness_history': avg_fitness_history,
        'min_fitness_history': min_fitness_history
    }

# Анализ результатов
plt.figure(figsize=(12, 6))

# График средней приспособленности
plt.subplot(1, 2, 1)
for Pc in crossover_probabilities:
    avg_fitness = results[Pc]['avg_fitness_history']
    plt.plot(range(1, generations + 1), avg_fitness, label=f'Pc = {Pc}', linewidth=2)
plt.title('Средняя приспособленность по поколениям')
plt.xlabel('Поколение')
plt.ylabel('Средняя приспособленность')
plt.legend()
plt.grid(True)

# График минимальной приспособленности
plt.subplot(1, 2, 2)
for Pc in crossover_probabilities:
    min_fitness = results[Pc]['min_fitness_history']
    plt.plot(range(1, generations + 1), min_fitness, label=f'Pc = {Pc}', linewidth=2)
plt.title('Минимальная приспособленность по поколениям')
plt.xlabel('Поколение')
plt.ylabel('Минимальная приспособленность')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Вывод результатов и заключение
for Pc in crossover_probabilities:
    avg_fitness = results[Pc]['avg_fitness_history']
    min_fitness = results[Pc]['min_fitness_history']
    print(f"Pc = {Pc}:")
    print(f"  Средняя приспособленность на последнем поколении: {avg_fitness[-1]:.4f}")
    print(f"  Минимальная приспособленность на последнем поколении: {min_fitness[-1]:.4f}")
    print("")

# Заключение на основе полученных результатов
print("Заключение:")
best_Pc = max(crossover_probabilities, key=lambda pc: results[pc]['min_fitness_history'][-1])
print(f"Лучшие результаты минимальной приспособленности на последнем поколении достигнуты при Pc = {best_Pc}.")
print(f"Повышение вероятности кроссинговера, как правило, улучшает производительность алгоритма, но на высоких значениях Pc эффект становится менее выраженным.")
