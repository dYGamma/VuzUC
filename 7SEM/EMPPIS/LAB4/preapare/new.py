import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Параметры алгоритма
params = {
    'generations': 100,        # Количество поколений
    'population_size': 300,    # Размер популяции
    'max_depth': 8,            # Максимальная глубина дерева
    'mutation_chance': 0.7     # Вероятность мутации
}

# Функция для оценки (первоначальная функция)
def fGold(x1, x2):
    return (1 + (x1 + x2 + 1)**2 * (19 - 14*x1 + 3*x1**2 - 14*x2 + 6*x1*x2 + 3*x2**2)) * \
           (30 + (2*x1 - 3*x2)**2 * (18 - 32*x1 + 12*x1**2 + 48*x2 - 36*x1*x2 + 27*x2**2))

# Поиск реального минимума функции 
def find_real_minimum(): 
    bounds = [(-2, 2), (-2, 2)] 
    result = minimize(lambda x: fGold(x[0], x[1]), [0, 0], bounds=bounds) 
    return result.fun, result.x
 
# Класс для узла дерева 
class Node: 
    def __init__(self, value, left=None, right=None): 
        self.value = value 
        self.left = left 
        self.right = right 
 
    def evaluate(self, x1, x2): 
        if self.value in ['+', '-', '*', '/', 'abs', 'sin', 'cos', 'exp']: 
            try: 
                left_value = self.left.evaluate(x1, x2) if self.left else None 
                right_value = self.right.evaluate(x1, x2) if self.right else None 
 
                if left_value is None or right_value is None: 
                    return None  # Пропускаем, если нет значений 
 
                if self.value == '+': 
                    return left_value + right_value 
                elif self.value == '-': 
                    return left_value - right_value 
                elif self.value == '*': 
                    return left_value * right_value 
                elif self.value == '/': 
                    if right_value == 0: 
                        return None  # Пропускаем деление на 0 
                    return left_value / right_value 
                elif self.value == 'abs': 
                    return abs(left_value) 
                elif self.value == 'sin': 
                    return np.sin(left_value) 
                elif self.value == 'cos': 
                    return np.cos(left_value) 
                elif self.value == 'exp': 
                    return np.exp(left_value) 
            except Exception: 
                return None  # Возвращаем None при ошибке 
        else: 
            return float(self.value) if isinstance(self.value, (int, float)) else (x1 if self.value == 'x1' else x2) 
        
    def __str__(self, level=0): 
        ret = "\t" * level + repr(self.value) + "\n" 
        if self.left: ret += self.left.__str__(level + 1) 
        if self.right: ret += self.right.__str__(level + 1) 
        return ret 
 
# Генерация случайного дерева 
def generate_tree(max_depth, current_depth=0): 
    if current_depth < max_depth and random.random() > 0.5: 
        func = random.choice(['+', '-', '*', '/', 'abs', 'sin', 'cos', 'exp']) 
        left = generate_tree(max_depth, current_depth + 1) 
        right = generate_tree(max_depth, current_depth + 1) 
        return Node(func, left, right) 
    else:  
        return Node(random.choice([random.uniform(-2, 2), 'x1', 'x2'])) 
 
# Оценка фитнеса особи 
def fitness(individual, real_minimum): 
    output = individual.evaluate(0, 0)  # Используем 0, 0 как заглушку 
    if output is None:  # Проверяем на None 
        return 0  
    return 1 / (1 + abs(output - real_minimum)) 
 
# Вероятность ошибки
def error_probability(found_value, real_minimum):
    return abs(found_value - real_minimum) / abs(real_minimum)

# Отбор родителей 
def select_parents(population, real_minimum): 
    weights = [fitness(ind, real_minimum) for ind in population] 
    return random.choices(population, weights=weights, k=2) 
 
# Кроссинговер 
def crossover(parent1, parent2): 
    # Обмен поддеревьями 
    child1 = Node(parent1.value) 
    child2 = Node(parent2.value) 
 
    child1.left, child1.right = parent1.left, parent2.right 
    child2.left, child2.right = parent2.left, parent1.right 
    return child1, child2 
 
# Мутация 
def mutate(individual, max_depth): 
    if random.random() < params['mutation_chance']:  # Шанс мутации 
        return generate_tree(max_depth)  # Генерируем новое дерево 
    return individual  # Если мутация не произошла, возвращаем оригинал 
 
# Основной алгоритм генетического программирования
def genetic_programming(): 
    population = [generate_tree(params['max_depth']) for _ in 
range(params['population_size'])] 
    best_fitnesses = [] 
    found_minima = [] 
 
    # Находим реальный минимум 
    real_minimum, _ = find_real_minimum() 
    print(f"Real Minimum Value: {real_minimum}") 
 
    # Переменные для хранения наилучшего индивидуума 
    best_overall_individual = None 
    best_overall_fitness = 0 
 
    for generation in range(params['generations']): 
        new_population = [] 
        for _ in range(params['population_size'] // 2): 
            parent1, parent2 = select_parents(population, real_minimum) 
            child1, child2 = crossover(parent1, parent2) 
            new_population.extend([mutate(child1, params['max_depth']), mutate(child2, params['max_depth'])]) 
         
        population = new_population 
         
        # Находим лучший фитнес в текущем поколении 
        best_individual = max(population, key=lambda ind: fitness(ind, real_minimum)) 
        found_minima.append(best_individual.evaluate(0, 0))  # Вычисляем значение функции 
        best_fitness = fitness(best_individual, real_minimum) 
        best_fitnesses.append(best_fitness) 
 
        # Обновляем наилучшего индивидуума за все поколения 
        if best_fitness > best_overall_fitness: 
            best_overall_fitness = best_fitness 
            best_overall_individual = best_individual 
 
        # Выводим древовидное представление лучшего индивидуума 
        print(f"\nGeneration {generation + 1}: Best Fitness = {best_fitness:.4f}, Best Value = {found_minima[-1]:.4f}") 
        print("Best Individual Tree Structure:") 
        print(best_individual) 
 
    # Вывод наилучшего результата из всех поколений 
    print("\nBest Overall Individual:") 
    print(best_overall_individual) 
    print(f"Best Overall Value: {best_overall_individual.evaluate(0, 0):.4f}") 
    print(f"Best Overall Fitness: {best_overall_fitness:.4f}")

    # Отображение графиков 
    plt.figure(figsize=(12, 5)) 
    # График 1: Прогресс фитнеса 
    plt.subplot(1, 2, 1) 
    plt.plot(range(1, params['generations'] + 1), best_fitnesses, label='Best Fitness') 
    plt.xlabel('Generations') 
    plt.ylabel('Best Fitness') 
    plt.title('Fitness Progression Over Generations') 
    plt.grid() 
    plt.legend() 
    # График 2: Найденные минимумы и реальный минимум 
    plt.subplot(1, 2, 2) 
    plt.plot(range(1, params['generations'] + 1), found_minima, label='Found Minima', 
    color='orange') 
    plt.axhline(real_minimum, color='red', linestyle='--', label='Real Minimum') 
    plt.xlabel('Generations') 
    plt.ylabel('Function Value') 
    plt.title('Found Minima Over Generations') 
    plt.grid() 
    plt.legend() 
    plt.tight_layout() 
    plt.show() 

if __name__ == "__main__":
    genetic_programming()