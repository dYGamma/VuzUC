import numpy as np
from scipy.stats import t

# Данные
X = np.array([4.9, 7.8, 4.1, 3.9, 2.0, 2.3, 0.7, 1.1, 1.6, 2.6])
Y = np.array([6.7, 5.0, 4.2, 2.6, 0.7, 1.7, 2.1, 3.9, 5.4, 6.9])

# Выборочные характеристики
mean_X = np.mean(X)
mean_Y = np.mean(Y)
var_X = np.var(X, ddof=1)
var_Y = np.var(Y, ddof=1)
n_X = len(X)
n_Y = len(Y)

# Стандартная ошибка разности средних
SE = np.sqrt(var_X / n_X + var_Y / n_Y)

# Статистика t
t_stat = (mean_X - mean_Y) / SE

# Критическое значение t
alpha = 0.05
df = n_X + n_Y - 2
t_critical = t.ppf(1 - alpha, df)

# Вывод результатов
print(f"Выборочное среднее X: {mean_X:.2f}")
print(f"Выборочное среднее Y: {mean_Y:.2f}")
print(f"Статистика t: {t_stat:.2f}")
print(f"Критическое значение t: {t_critical:.2f}")

if t_stat > t_critical:
    print("Нулевая гипотеза отвергается. M(X) > M(Y).")
else:
    print("Нет оснований отвергать нулевую гипотезу.")