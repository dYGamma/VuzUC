import numpy as np
import matplotlib.pyplot as plt

# Параметры
x_start = np.pi / 4
x_end = np.pi / 2
num_points = 100
x_values = np.linspace(x_start, x_end, num_points)

# Граничные условия
y_start = -np.log(np.sqrt(2))
y_end = 0

# Начальная оценка функции y
y_values = np.ones(num_points)  # Начнем с константы y = 1

# Итерационный процесс для нахождения оптимального решения
tolerance = 1e-6
max_iterations = 1000
for iteration in range(max_iterations):
    # Обновление значений y
    y_new = np.zeros_like(y_values)
    
    for i in range(1, num_points - 1):
        # Используем уравнение Эйлера-Лагранжа
        y_new[i] = y_values[i] - 0.01 * np.sin(x_values[i]) * (1 - y_values[i])
    
    # Установка граничных условий
    y_new[0] = y_start
    y_new[-1] = y_end
    
    # Проверка на сходимость
    if np.max(np.abs(y_new - y_values)) < tolerance:
        break
    
    y_values = y_new

# Вывод значений y(x)
for x, y in zip(x_values, y_values):
    print(f"x: {x:.4f}, y(x): {y:.4f}")

# Визуализация результата
plt.plot(x_values, y_values, label='Оптимальное решение y(x)')
plt.axhline(y_start, color='r', linestyle='--', label='Граничное условие y(π/4)')
plt.axhline(y_end, color='g', linestyle='--', label='Граничное условие y(π/2)')
plt.title('Решение вариационной задачи')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()
