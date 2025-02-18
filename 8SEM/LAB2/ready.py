import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2

# Данные из варианта 96
intervals = [(-0.3, -0.2), (-0.2, -0.1), (-0.1, 0), (0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4)]
m_i = [2, 14, 25, 27, 17, 11, 4]
n = sum(m_i)  # Общее количество наблюдений

# Шаг 1: Статистические вероятности
p_i = [m / n for m in m_i]

# Шаг 2: Плотности вероятности для гистограммы
delta_x = intervals[0][1] - intervals[0][0]  # Длина интервала
f_i = [p / delta_x for p in p_i]

# Середины интервалов
midpoints = [(a + b) / 2 for a, b in intervals]

# Построение гистограммы
plt.bar(midpoints, f_i, width=delta_x, alpha=0.6, color='blue', edgecolor='black', label='Экспериментальная гистограмма')

# Шаг 3: Теоретическая плотность нормального распределения
# Метод моментов: вычисление mu и sigma
mu = sum(mid * m for mid, m in zip(midpoints, m_i)) / n
sigma_squared = sum(((mid - mu) ** 2) * m for mid, m in zip(midpoints, m_i)) / n
sigma = np.sqrt(sigma_squared)

print(f"Математическое ожидание (mu): {mu:.4f}")
print(f"Стандартное отклонение (sigma): {sigma:.4f}")

# Теоретическая плотность нормального распределения
x_theory = np.linspace(-0.3, 0.4, 500)
f_theory = norm.pdf(x_theory, loc=mu, scale=sigma)

# Добавление теоретической кривой на график
plt.plot(x_theory, f_theory, color='red', linewidth=2, label='Теоретическая плотность')

# Настройка графика
plt.title("Гистограмма и теоретическая плотность")
plt.xlabel("Значения случайной величины")
plt.ylabel("Плотность вероятности")
plt.legend()
plt.grid()
plt.show()

# Шаг 4: Проверка гипотезы о нормальном распределении (критерий хи-квадрат)
# Теоретические частоты
theoretical_probabilities = [norm.cdf(b, loc=mu, scale=sigma) - norm.cdf(a, loc=mu, scale=sigma) for a, b in intervals]
theoretical_frequencies = [p * n for p in theoretical_probabilities]

# Статистика хи-квадрат
chi2_stat = sum(((m - n_theor) ** 2) / n_theor for m, n_theor in zip(m_i, theoretical_frequencies))
degrees_of_freedom = len(intervals) - 1 - 2  # k = n - 1 - r (r = 2 для нормального распределения)
alpha = 0.025  # Уровень значимости для четных вариантов
chi2_critical = chi2.ppf(1 - alpha, degrees_of_freedom)

print(f"Статистика хи-квадрат: {chi2_stat:.4f}")
print(f"Критическое значение хи-квадрат: {chi2_critical:.4f}")

# Вывод результата проверки гипотезы
if chi2_stat < chi2_critical:
    print("Гипотеза о нормальном распределении принимается.")
else:
    print("Гипотеза о нормальном распределении отвергается.")