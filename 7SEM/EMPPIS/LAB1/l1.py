import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # или 'TkAgg', в зависимости от вашей системы
import matplotlib.pyplot as plt

def f(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.sin(2 * x) / (x ** 2)
        result[np.isnan(result)] = 0  # Обрабатываем NaN, если x=0
    return result

# Настройки
population_size = 100
generations = 50
mutation_rate = 0.2
mutation_chance = 0.9
x_bounds = [-20, -3.1]

# Инициализация популяции
population = np.random.uniform(x_bounds[0], x_bounds[1], population_size)

fitness_history = []
population_history = []

for generation in range(generations):
    fitness = f(population)
    fitness_history.append(fitness)
    population_history.append(population)
    
    selected_indices = np.argsort(fitness)[-population_size // 2:]
    selected_population = population[selected_indices]
    
    offspring = []
    for i in range(len(selected_population) // 2):
        parent1 = selected_population[2 * i]
        parent2 = selected_population[2 * i + 1]
        crossover_point = np.random.rand()
        child = crossover_point * parent1 + (1 - crossover_point) * parent2
        offspring.append(child)
    
    offspring = np.array(offspring)
    if np.random.uniform(0, 1) <= mutation_chance:
        mutation = np.random.uniform(-mutation_rate, mutation_rate, offspring.shape)
        offspring += mutation
    
    population = np.concatenate((selected_population, offspring))

# Функция для визуализации
def plot_generation(generation):
    print(fitness_history[generation])
    print(population_history[generation])
    plt.figure(figsize=(10, 6))
    plt.plot(population_history[generation], fitness_history[generation], 'o', label=f'Поколение {generation + 1}', alpha=0.7)
    
    x_values = np.linspace(x_bounds[0], x_bounds[1], 400)
    plt.plot(x_values, f(x_values), label='Исходная функция', color='red', linewidth=2)
    
    plt.title(f'Приспособленность индивидов в поколении {generation + 1}')
    plt.xlabel('Индивид')
    plt.ylabel('Приспособленность')
    plt.ylim(-0.5, 1)
    plt.legend(loc='upper right', fontsize='small')
    plt.grid()
    plt.show()

while True:
    user_input = input("Введите номер поколения (1-50) или 'all' для отображения всех поколений: ")
    
    if user_input.lower() == 'q':
        break
    if user_input.lower() == 'all':
        plt.figure(figsize=(12, 8))
        for i in range(generations):
            plt.plot(population_history[i], fitness_history[i], 'o', label=f'Поколение {i + 1}', alpha=0.5)

        x_values = np.linspace(x_bounds[0], x_bounds[1], 400)
        plt.plot(x_values, f(x_values), label='Исходная функция', color='red', linewidth=2)

        plt.title(f'Приспособленность индивидов на протяжении {generations} поколений')
        plt.xlabel('Индивид')
        plt.ylabel('Приспособленность')
        plt.ylim(-0.5, 1)
        plt.legend(loc='upper right', fontsize='small')
        plt.grid()
        plt.show()
        # Сбор данных для расчета R^2
        x_true = np.linspace(x_bounds[0], x_bounds[1], 400)
        y_true = f(x_true)

        # Предсказанные значения
        y_pred = f(np.array(population_history))  # Применяем функцию f ко всем лучшим решениям

        # Вычисляем R^2
        SS_res = np.sum((y_true - y_pred[:, None])**2, axis=1)  # Остатки для каждого поколения
        SS_tot = np.sum((y_true - np.mean(y_true))**2)  # Общая сумма квадратов

        R_squared = 1 - (SS_res / SS_tot)
        print("Значения R^2 для каждого поколения:")
        print(R_squared)

        # Проверка, превышает ли среднее R^2 0.6
        average_R_squared = np.mean(R_squared)
        print(f"Среднее значение R^2: {average_R_squared:.2f}")
        if average_R_squared > 0.6:
            print("Среднее значение R^2 больше 0.6.")
        else:
            print("Среднее значение R^2 меньше или равно 0.6.")
    else:
        try:
            generation_number = int(user_input) - 1
            if 0 <= generation_number < generations:
                plot_generation(generation_number)
            else:
                print(f"Пожалуйста, введите номер поколения от 1 до {generations}.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите номер поколения или 'all'.")
