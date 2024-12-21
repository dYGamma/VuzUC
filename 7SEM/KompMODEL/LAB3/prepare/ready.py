# Импорт необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Данные для задачи из варианта 14
t = np.array([1, 2, 3, 4, 5, 6, 7])  # Время t (14 дней на шаг)
Y_t = np.array([115113.8, 116620.5, 117377.2, 116770.5, 118621.8, 118173.4, 118447])  # Стоимость Y(t)

# 1. Реализация МНК для полинома второй степени вручную
# Формирование матрицы X для полинома второй степени
X_poly_2 = np.vstack([t**2, t, np.ones(len(t))]).T

# Расчет коэффициентов МНК: a = (X^T * X)^(-1) * X^T * Y
coeffs_2 = np.linalg.inv(X_poly_2.T @ X_poly_2) @ X_poly_2.T @ Y_t

# Использование коэффициентов для предсказания значений
Y_pred_2 = coeffs_2[0] * t**2 + coeffs_2[1] * t + coeffs_2[2]

# Вычисление коэффициента детерминации R^2 для полинома второй степени
ss_total = np.sum((Y_t - np.mean(Y_t))**2)
ss_residual_2 = np.sum((Y_t - Y_pred_2)**2)
r2_2 = 1 - (ss_residual_2 / ss_total)

# 2. Подбор степени p для полиномиальной модели и оценка R²
degrees = [1, 2, 3, 4]
models = {}
r2_results = {}
adj_r2_results = {}

for degree in degrees:
    # Формирование матрицы X для данной степени
    X_poly = np.vstack([t**i for i in range(degree, -1, -1)]).T
    # Расчет коэффициентов МНК
    coeffs = np.linalg.inv(X_poly.T @ X_poly) @ X_poly.T @ Y_t
    # Сохранение модели и предсказаний
    models[degree] = coeffs
    Y_pred = np.polyval(coeffs, t)
    # Вычисление R² и скорректированного R²
    r2 = r2_score(Y_t, Y_pred)
    adj_r2 = 1 - (1 - r2) * (len(Y_t) - 1) / (len(Y_t) - degree - 1)
    r2_results[degree] = r2
    adj_r2_results[degree] = adj_r2

# 3. Аппроксимация функциональной зависимости вида f3(x)
def functional_model(x):
    return (3/7) * x ** 2 + x + 1

Y_f3 = functional_model(t)
r2_f3 = r2_score(Y_t, Y_f3)
adj_r2_f3 = 1 - (1 - r2_f3) * (len(Y_t) - 1) / (len(Y_t) - 2 - 1)

# 4. Прогноз на один шаг вперед (t=8)
next_step = 8
# Прогноз для полинома второй степени
Y_next_year_pred_2 = coeffs_2[0] * next_step**2 + coeffs_2[1] * next_step + coeffs_2[2]

# Прогноз для лучшей модели (на основании наилучшего R²_adj)
best_degree = max(adj_r2_results, key=adj_r2_results.get)
best_coeffs = models[best_degree]
Y_next_year_pred_best = np.polyval(best_coeffs, next_step)

# 5. Визуализация
plt.figure(figsize=(10, 6))
plt.scatter(t, Y_t, color='blue', label='Исходные данные')

# Графики моделей
x_range = np.linspace(1, 8, 100)
for degree, coeffs in models.items():
    plt.plot(x_range, np.polyval(coeffs, x_range), label=f'Полином {degree}-й степени')

# График функции f3(x)
plt.plot(x_range, functional_model(x_range), label='Функция f3(x)', linestyle='--', color='purple')

# Отображение прогноза
plt.scatter(next_step, Y_next_year_pred_2, color='red', label='Прогноз f1(t=8)', zorder=5)
plt.scatter(next_step, Y_next_year_pred_best, color='green', edgecolor='black', s=100, label=f'Прогноз (лучшая модель)')

plt.title('Модели и прогноз стоимости 1 м²')
plt.xlabel('Время (t)')
plt.ylabel('Стоимость Y(t)')
plt.legend()
plt.grid()
plt.show()

# 6. Вывод статистики
print("\nПОДРОБНАЯ СТАТИСТИКА:")
print(f"- Полином второй степени (f1): R^2 = {r2_2:.4f}, Скорректированный R^2 = {1 - (1 - r2_2) * (len(Y_t) - 1) / (len(Y_t) - 3):.4f}")

for degree, r2 in r2_results.items():
    adj_r2 = adj_r2_results[degree]
    print(f"Полином {degree}-й степени: R2 = {r2:.4f}, Adjusted R2 = {adj_r2:.4f}")

print(f"\nЗаданная модель f3(x): R2 = {r2_f3:.4f}, Скорректированный R2 = {adj_r2_f3:.4f}")

print("\nПРОГНОЗ НА t=8:")
print(f"- Полином второй степени: {Y_next_year_pred_2:.2f} руб.")
print(f"- Лучшая модель (степень {best_degree}): {Y_next_year_pred_best:.2f} руб.")

