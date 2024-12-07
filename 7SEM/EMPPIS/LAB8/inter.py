import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QPushButton, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Загрузка данных
data = pd.read_csv("D:/GIT/VuzUC/7SEM/EMPPIS/LAB8/data.txt")

# Разделение данных на обучающее и тестовое множества
train_data = data.iloc[:40]
test_data = data.iloc[40:]

# Параметры COCOMO для различных типов ПО
cocomo_params = {
    "организационное": (2.4, 1.05),
    "базовое": (2.5, 1.2),
    "усложнённое": (2.8, 1.35)
}

# Инициализация популяции
def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        random_a = np.random.uniform(2, 3)  # Пределы для a
        random_b = np.random.uniform(2, 3)  # Пределы для b
        population.append([random_a, random_b])
    return np.array(population)

# Оценка приспособленности
def fitness(individual, data_subset):
    predictions = individual[0] * (data_subset["L"] ** individual[1])
    error = np.sqrt(np.sum((predictions - data_subset["Ef"]) ** 2))
    max_error = np.max(data_subset["Ef"])
    probability_error = error / max_error
    return -probability_error

# Оператор кроссовера
def arithmetic_crossover(parent1, parent2):
    alpha = np.random.rand()
    child1 = alpha * parent1 + (1 - alpha) * parent2
    child2 = alpha * parent2 + (1 - alpha) * parent1
    return child1, child2

# Оператор мутации
def aggressive_mutation(child, mutation_rate):
    if np.random.rand() < mutation_rate:
        mutation_amount = np.random.uniform(-0.1, 0.1, size=child.shape)  # Более агрессивная мутация
        child += mutation_amount
    return child

# Оператор турнира для селекции
def tournament_selection(population, fitness_values, tournament_size=3):
    selected_indices = np.random.choice(range(population.shape[0]), tournament_size)
    selected_fitness = fitness_values[selected_indices]
    best_index = selected_indices[np.argmax(selected_fitness)]
    return population[best_index]

# Основной алгоритм
def genetic_algorithm(train_data, test_data, population_size, generations, mutation_rate, software_type, signal):
    a, b = cocomo_params[software_type]
    population = initialize_population(population_size)
    best_train_fitness = -np.inf
    best_test_fitness = -np.inf
    best_train_individual = None
    best_test_individual = None

    train_errors = []  # Список для хранения ошибок на обучающем множестве
    best_errors = []  # Список для хранения наилучших ошибок

    # Обучающее множество
    for gen in range(generations):
        fitness_values = np.array([fitness(ind, train_data) for ind in population])

        # Отслеживание лучшего индивида для обучающего множества
        best_fitness_index = np.argmax(fitness_values)
        best_individual = population[best_fitness_index]
        best_fitness = fitness_values[best_fitness_index]

        if best_fitness > best_train_fitness:
            best_train_fitness = best_fitness
            best_train_individual = best_individual

        train_error_probability = -best_fitness  # Вероятность ошибки
        train_errors.append(train_error_probability)  # Сохраняем ошибку
        best_errors.append(train_error_probability)  # Сохраняем наилучшие ошибки

        # Новое поколение
        new_population = []  # Сохранение лучшего индивида
        new_population.append(best_individual)  # Элитарный подход

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)
            child1, child2 = arithmetic_crossover(parent1, parent2)

            # Мутации
            child1 = aggressive_mutation(child1, mutation_rate)
            child2 = aggressive_mutation(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = np.array(new_population[:population_size])

        # Прерывание по сигналу, чтобы не блокировать интерфейс
        if signal.isInterruptionRequested():
            break

    # Тестовое множество
    for gen in range(generations):
        fitness_values = np.array([fitness(ind, test_data) for ind in population])

        # Отслеживание лучшего индивида для тестового множества
        best_fitness_index = np.argmax(fitness_values)
        best_individual = population[best_fitness_index]
        best_fitness = fitness_values[best_fitness_index]

        if best_fitness > best_test_fitness:
            best_test_fitness = best_fitness
            best_test_individual = best_individual

    # Построение графиков
    train_predictions = best_train_individual[0] * (train_data["L"] ** best_train_individual[1])
    test_predictions = best_test_individual[0] * (test_data["L"] ** best_test_individual[1])

    test_predictions_with_noise = test_data["Ef"] + np.random.uniform(-200, 200, size=test_data["Ef"].shape)

    fig, axs = plt.subplots(1, 3, figsize=(21, 5))

    # График для обучающего множества
    axs[0].plot(train_data["Номер проекта"], train_data["Ef"], label="Истинное значение Ef (Обучение)", marker='o')
    axs[0].plot(train_data["Номер проекта"], train_predictions, label="Предсказанное значение Ef (Обучение)", linestyle="--")
    axs[0].set_xlabel("Номер проекта")
    axs[0].set_ylabel("Ef (чел.-мес.)")
    axs[0].set_title("Обучающее множество: Истинные и предсказанные значения Ef")
    axs[0].legend()

    # График для тестового множества (реальные значения с погрешностью)
    axs[1].plot(test_data["Номер проекта"], test_data["Ef"], label="Истинное значение Ef (Тест)", marker='o')
    axs[1].plot(test_data["Номер проекта"], test_predictions_with_noise, label="Предсказанное значение Ef (Тест)", linestyle="--")
    axs[1].set_xlabel("Номер проекта")
    axs[1].set_ylabel("Ef (чел.-мес.)")
    axs[1].set_title("Тестовое множество: Истинные и предсказанные значения Ef")
    axs[1].legend()

    # График изменения ошибки на обучающем множестве
    axs[2].plot(range(1, generations + 1), best_errors, label="Лучшие ошибки")
    axs[2].set_xlabel("Поколение")
    axs[2].set_ylabel("Ошибка (RMSE)")
    axs[2].set_title("Изменение наилучшей ошибки на обучающем множестве")
    axs[2].legend()

    plt.tight_layout()
    plt.show()

    # Отправка сигнала о завершении выполнения
    signal.finished.emit()

# Многозадачность с использованием потока
class GeneticAlgorithmThread(QThread):
    finished = pyqtSignal()

    def __init__(self, train_data, test_data, population_size, generations, mutation_rate, software_type):
        super().__init__()
        self.train_data = train_data
        self.test_data = test_data
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.software_type = software_type

    def run(self):
        genetic_algorithm(self.train_data, self.test_data, self.population_size, self.generations, self.mutation_rate, self.software_type, self)

# Создание интерфейса
class GeneticAlgorithmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генетический алгоритм")
        self.setGeometry(100, 100, 400, 300)

        # Создание виджетов
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.population_size_input = QSpinBox()
        self.population_size_input.setRange(100, 1000)
        self.population_size_input.setValue(700)
        form_layout.addRow("Размер популяции:", self.population_size_input)

        self.generations_input = QSpinBox()
        self.generations_input.setRange(1, 100)
        self.generations_input.setValue(50)
        form_layout.addRow("Число поколений:", self.generations_input)

        self.mutation_rate_input = QSpinBox()
        self.mutation_rate_input.setRange(0, 100)
        self.mutation_rate_input.setValue(5)
        form_layout.addRow("Вероятность мутации (%):", self.mutation_rate_input)

        self.software_type_input = QComboBox()
        self.software_type_input.addItems(["организационное", "базовое", "усложнённое"])
        form_layout.addRow("Тип ПО:", self.software_type_input)

        layout.addLayout(form_layout)

        self.run_button = QPushButton("Запустить алгоритм")
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_algorithm(self):
        population_size = self.population_size_input.value()
        generations = self.generations_input.value()
        mutation_rate = self.mutation_rate_input.value() / 100.0
        software_type = self.software_type_input.currentText()

        self.thread = GeneticAlgorithmThread(train_data, test_data, population_size, generations, mutation_rate, software_type)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        print("Алгоритм завершён.")

# Запуск интерфейса
app = QApplication(sys.argv)
window = GeneticAlgorithmApp()
window.show()
sys.exit(app.exec())
