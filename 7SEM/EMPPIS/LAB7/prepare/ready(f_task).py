import numpy as np
import matplotlib.pyplot as plt
import time

# Определение функции Эасома
# Функция Эасома имеет известный минимум в точке (π, π) со значением -1
def easom_function(position):
    x1, x2 = position
    return -np.cos(x1) * np.cos(x2) * np.exp(-((x1 - np.pi)**2 + (x2 - np.pi)**2))

# Параметры алгоритма PSO
num_particles = 100            # Число частиц в популяции
num_iterations = 100           # Общее число итераций алгоритма
inertia_weight = 0.5           # Коэффициент инерции для регулировки "тяжести" скорости
cognitive_coeff = 1.5          # Когнитивный коэффициент (влияние личного опыта частицы)
social_coeff = 1.5             # Социальный коэффициент (влияние группы на частицу)
lower_bound, upper_bound = 0, 2 * np.pi  # Границы области поиска (x1 и x2)

# Инициализация позиций и скоростей частиц
positions = np.random.uniform(lower_bound, upper_bound, (num_particles, 2))  # Случайные начальные позиции
velocities = np.random.uniform(-1, 1, (num_particles, 2))  # Случайные начальные скорости

# Лучшая позиция для каждой частицы (личный опыт)
personal_best_positions = positions.copy()
personal_best_scores = np.array([easom_function(pos) for pos in positions])  # Значения функции для личных лучших позиций

# Глобальная лучшая позиция (опыт всей группы)
global_best_position = positions[np.argmin(personal_best_scores)]
global_best_score = np.min(personal_best_scores)

# Создание сетки для отображения поверхности функции
x_vals = np.linspace(lower_bound, upper_bound, 200)
y_vals = np.linspace(lower_bound, upper_bound, 200)
x_grid, y_grid = np.meshgrid(x_vals, y_vals)
z_grid = easom_function([x_grid, y_grid])

# Настройка графика
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Построение поверхности функции Эасома
surface = ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none')
ax.set_xlim([lower_bound, upper_bound])
ax.set_ylim([lower_bound, upper_bound])
ax.set_zlim([-1.5, 0.5])
ax.view_init(elev=30, azim=240)  # Установка угла обзора
ax.set_title('PSO оптимизация функции Эасома', fontsize=16)
ax.set_xlabel('x1', fontsize=14)
ax.set_ylabel('x2', fontsize=14)
ax.set_zlabel('f(x1, x2)', fontsize=14)

# Основной цикл алгоритма PSO
for iter_num in range(num_iterations):
    print(f"Итерация {iter_num + 1}/{num_iterations}")  # Вывод текущей итерации
    for particle_idx in range(num_particles):
        # Расчёт когнитивной и социальной составляющих для обновления скорости
        cognitive_term = cognitive_coeff * np.random.rand() * (personal_best_positions[particle_idx] - positions[particle_idx])
        social_term = social_coeff * np.random.rand() * (global_best_position - positions[particle_idx])

        # Обновление скорости частицы
        velocities[particle_idx] = (inertia_weight * velocities[particle_idx] + 
                                    cognitive_term + 
                                    social_term)

        # Обновление позиции частицы и ограничение в пределах области поиска
        positions[particle_idx] += velocities[particle_idx]
        positions[particle_idx] = np.clip(positions[particle_idx], lower_bound, upper_bound)

        # Вычисление значения функции для новой позиции
        current_fitness = easom_function(positions[particle_idx])

        # Если новое значение лучше личного, обновляем личный лучший результат
        if current_fitness < personal_best_scores[particle_idx]:
            personal_best_scores[particle_idx] = current_fitness
            personal_best_positions[particle_idx] = positions[particle_idx]

    # Обновление глобального лучшего результата
    best_particle_idx = np.argmin(personal_best_scores)
    if personal_best_scores[best_particle_idx] < global_best_score:
        global_best_score = personal_best_scores[best_particle_idx]
        global_best_position = personal_best_positions[best_particle_idx]

    # Вывод информации о текущем лучшем результате
    print(f"Лучший результат на итерации {iter_num + 1}: f({global_best_position[0]:.6f}, {global_best_position[1]:.6f}) = {global_best_score:.6f}")

    # Визуализация текущего состояния частиц на графике
    ax.scatter(positions[:, 0], positions[:, 1], [easom_function(pos) for pos in positions], color='blue', alpha=0.3)
    plt.pause(0.1)  # Пауза для обновления визуализации

# Отображение финального результата на графике
ax.scatter(global_best_position[0], global_best_position[1], global_best_score, color='red', s=100, label='Найденный минимум (PSO)')
ax.scatter(np.pi, np.pi, -1, color='green', s=100, label='Известный минимум')
ax.legend(loc='upper right')
plt.show()

# Вывод результатов оптимизации
print(f'Найденный минимум: x1 = {global_best_position[0]:.6f}, x2 = {global_best_position[1]:.6f}')
print(f'Значение функции в найденной точке: {global_best_score:.6f}')
print(f'Глобальный минимум: f(x1, x2) = -1 при x1 = pi, x2 = pi')
