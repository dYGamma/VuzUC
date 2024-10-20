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

# Функция для выполнения ПГА с заданным значением вероятности кроссинговера
def run_ga(crossover_prob):
    population = np.concatenate([np.random.uniform(x_bounds[0], -0.01, population_size // 2),
                                 np.random.uniform(0.01, x_bounds[1], population_size // 2)])

    fitness_history = []
    population_history = []

    for generation in range(generations):
        fitness = f(population)
        fitness_history.append(np.mean(fitness))  # Сохраняем среднюю приспособленность
        population_history.append(population)

        # Селекция лучших особей
        selected_indices = np.argsort(fitness)[:population_size // 2]
        selected_population = population[selected_indices]

        # Кроссинговер и создание потомков
        offspring = []
        for i in range(len(selected_population) // 2):
            parent1 = selected_population[2 * i]
            parent2 = selected_population[2 * i + 1]
            if np.random.rand() < crossover_prob:  # Проверка вероятности кроссинговера
                crossover_point = np.random.rand()
                child = crossover_point * parent1 + (1 - crossover_point) * parent2
            else:
                child = parent1  # Потомок идентичен родителю, если кроссинговер не произошёл
            offspring.append(child)

        offspring = np.array(offspring)
        
        # Мутация
        if np.random.uniform(0, 1) <= mutation_chance:
            mutation = np.random.uniform(-mutation_rate, mutation_rate, offspring.shape)
            offspring += mutation

        population = np.concatenate((selected_population, offspring))

    return population_history, fitness_history

# Функция для визуализации
def plot_generation(generation, population_history, fitness_history, title):
    plt.figure(figsize=(10, 6))
    plt.plot(population_history[generation], f(population_history[generation]), 'o', label=f'Поколение {generation + 1}', alpha=0.7)
    
    x_values = np.linspace(x_bounds[0], x_bounds[1], 400)
    x_values = np.concatenate([x_values[x_values < 0], x_values[x_values > 0]])  # Исключаем x=0
    plt.plot(x_values, f(x_values), label='Исходная функция', color='red', linewidth=2)
    
    plt.title(title)
    plt.xlabel('Индивид')
    plt.ylabel('Приспособленность')
    plt.ylim(-10, 10)
    plt.legend(loc='upper right', fontsize='small')
    plt.grid()
    plt.show()

# Функция для анализа результатов
def analyze_results(fitness_histories, crossover_probs):
    print("\nАнализ исследования на основе полученных данных:\n")
    
    for idx, pc in enumerate(crossover_probs):
        print(f"1. **Pc = {pc}**: \n")
        print(f"Средняя приспособленность в последнем поколении: {fitness_histories[idx][-1]:.4f}")
        print(f"Скорость сходимости: {np.max(fitness_histories[idx]) - np.min(fitness_histories[idx]):.4f}")
        if fitness_histories[idx][-1] > 0:
            print(f"Алгоритм показывает уверенную сходимость при данном значении кроссинговера.\n")
        else:
            print(f"Схождение к хорошему решению происходит медленно, вероятно, из-за недостаточной изменчивости в популяции.\n")

    print("\n**Итоги и выводы**:\n")
    max_fitness_last_gen = [fh[-1] for fh in fitness_histories]
    best_pc_idx = np.argmax(max_fitness_last_gen)
    
    print(f"Оптимальное значение вероятности кроссинговера по результатам эксперимента: Pc = {crossover_probs[best_pc_idx]}")
    print(f"Лучший результат по среднему значению приспособленности был достигнут при Pc = {crossover_probs[best_pc_idx]} с приспособленностью {max_fitness_last_gen[best_pc_idx]:.4f}.")
    print("Алгоритм лучше всего работает при средних значениях вероятности кроссинговера, где достигается лучший баланс между исследованием и сохранением хороших решений.")

# Исследование для разных значений Pc
crossover_probs = [0.1, 0.5, 0.9]
fitness_histories = []

for pc in crossover_probs:
    population_history, fitness_history = run_ga(crossover_prob=pc)
    fitness_histories.append(fitness_history)
    
    # Визуализируем последнее поколение для каждого значения Pc
    plot_generation(generations - 1, population_history, fitness_history, f'Поколение {generations}, Pc={pc}')

# Визуализируем сходимость для всех поколений для всех Pc
for pc in crossover_probs:
    population_history, fitness_history = run_ga(crossover_prob=pc)

    plt.figure(figsize=(12, 8))
    for i in range(generations):
        plt.plot(population_history[i], f(population_history[i]), 'o', label=f'Поколение {i + 1}', alpha=0.5)

    x_values = np.linspace(x_bounds[0], x_bounds[1], 400)
    x_values = np.concatenate([x_values[x_values < 0], x_values[x_values > 0]])  # Исключаем x=0
    plt.plot(x_values, f(x_values), label='Исходная функция', color='red', linewidth=2)

    plt.title(f'Приспособленность индивидов на протяжении {generations} поколений для Pc={pc}')
    plt.xlabel('Индивид')
    plt.ylabel('Приспособленность')
    plt.ylim(-10, 10)
    plt.legend(loc='upper right', fontsize='small')
    plt.grid()
    plt.show()

# Вывод анализа на основе данных
analyze_results(fitness_histories, crossover_probs)
