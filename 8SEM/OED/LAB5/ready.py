import numpy as np
import scipy.stats as stats

# Исходные данные
# Экспериментальные наблюдения:
#   x1: 2, 3, 4, 6, 7, -1
#   x2: -2, 0, 1, 2, 3, -1
#   y : 16, 6, 1, -2, -8, 7

x1 = np.array([2, 3, 4, 6, 7, -1])
x2 = np.array([-2, 0, 1, 2, 3, -1])
y  = np.array([16, 6, 1, -2, -8, 7])
n = len(y)

print("Исходные данные:")
print("x1 =", x1)
print("x2 =", x2)
print("y  =", y)
print("\n-----------------------------")

# 1. Центрирование факторов (вычитание среднего)
mean_x1 = np.mean(x1)
mean_x2 = np.mean(x2)
x1_centered = x1 - mean_x1
x2_centered = x2 - mean_x2

print("Центрированные факторы:")
print("x1_centered =", x1_centered)
print("x2_centered =", x2_centered)
print("\n-----------------------------")

# 2. Построение дизайн-матрицы X (свободный член + центрированные факторы)
# X имеет вид: [1, x1_centered, x2_centered]
X = np.column_stack((np.ones(n), x1_centered, x2_centered))
k = 2  # число факторов

# 3. Оценка коэффициентов регрессии (метод наименьших квадратов)
# Нормальное уравнение: beta_hat = (X^T X)^(-1) X^T y
XtX = X.T @ X
XtX_inv = np.linalg.inv(XtX)
beta_hat = XtX_inv @ (X.T @ y)

print("Оценки коэффициентов регрессии:")
print("beta0 (интерсепт) =", beta_hat[0])
print("beta1           =", beta_hat[1])
print("beta2           =", beta_hat[2])
print("\nУравнение регрессии:")
print("y = {:.4f} + {:.4f}*(x1 - {:.4f}) + {:.4f}*(x2 - {:.4f})".format(
    beta_hat[0], beta_hat[1], mean_x1, beta_hat[2], mean_x2))
print("\n-----------------------------")

# 4. Проверка адекватности модели по критерию Фишера
# Вычисляем предсказанные значения, остатки, RSS, ESS и TSS.
y_pred = X @ beta_hat
residuals = y - y_pred
RSS = np.sum(residuals**2)
TSS = np.sum((y - np.mean(y))**2)
ESS = TSS - RSS

# Степени свободы: регрессии (число факторов) и ошибок (n - число параметров)
df_reg = k         # число степеней свободы регрессии (без учета свободного члена)
df_error = n - (k + 1)
MSE = RSS / df_error

# Статистика Фишера: F = (ESS/k) / (RSS/df_error)
F_stat = (ESS / df_reg) / MSE

alpha = 0.05
F_crit = stats.f.ppf(1 - alpha, df_reg, df_error)

print("Проверка адекватности модели (критерий Фишера):")
print("RSS =", RSS)
print("TSS =", TSS)
print("ESS =", ESS)
print("Степени свободы регрессии =", df_reg, ", степени свободы ошибок =", df_error)
print("MSE =", MSE)
print("F статистика =", F_stat)
print("Критическое F (при α = 0.05) =", F_crit)
if F_stat > F_crit:
    print("Модель адекватна на уровне значимости α =", alpha)
else:
    print("Модель неадекватна на уровне значимости α =", alpha)
print("\n-----------------------------")

# 5. Проверка значимости факторов по критерию Стьюдента
# Для каждого коэффициента вычисляем стандартную ошибку, t-статистику и p-value.
SE_beta = np.sqrt(np.diag(MSE * XtX_inv))
t_stats = beta_hat / SE_beta
p_values = [2 * (1 - stats.t.cdf(np.abs(t), df=df_error)) for t in t_stats]

print("Проверка значимости коэффициентов (критерий Стьюдента):")
print("Стандартные ошибки коэффициентов:", SE_beta)
print("t-статистики коэффициентов:", t_stats)
print("p-value для коэффициентов:", p_values)
print("\n(Значимым считается фактор, если p-value < 0.05)")
# Обычно интерсепт не исключают, поэтому проверяем факторы beta1 и beta2:
insignificant = []
if p_values[1] > alpha:
    insignificant.append(1)
if p_values[2] > alpha:
    insignificant.append(2)
print("Незначимые факторы (индексы коэффициентов):", insignificant)
print("\n-----------------------------")

# 6. Селекция факторов: если есть незначимые, исключаем их и повторно оцениваем модель.
if insignificant:
    cols = [0] + [i for i in range(1, len(beta_hat)) if i not in insignificant]
    X_new = X[:, cols]
    XtX_new = X_new.T @ X_new
    XtX_inv_new = np.linalg.inv(XtX_new)
    beta_hat_new = XtX_inv_new @ (X_new.T @ y)
    
    print("После исключения незначимых факторов:")
    for i, col in enumerate(cols):
        if col == 0:
            print("beta0 (интерсепт) =", beta_hat_new[i])
        else:
            print("beta{}".format(col), "=", beta_hat_new[i])
    
    # Пересчёт критериев для новой модели
    y_pred_new = X_new @ beta_hat_new
    residuals_new = y - y_pred_new
    RSS_new = np.sum(residuals_new**2)
    df_error_new = n - X_new.shape[1]
    MSE_new = RSS_new / df_error_new
    TSS_new = np.sum((y - np.mean(y))**2)
    ESS_new = TSS_new - RSS_new
    df_reg_new = X_new.shape[1] - 1
    F_stat_new = (ESS_new / df_reg_new) / MSE_new if df_reg_new > 0 else np.nan
    F_crit_new = stats.f.ppf(1 - alpha, df_reg_new, df_error_new) if df_reg_new > 0 else np.nan
    
    print("\nНовая проверка адекватности модели (критерий Фишера):")
    print("RSS =", RSS_new)
    print("TSS =", TSS_new)
    print("ESS =", ESS_new)
    print("Степени свободы регрессии =", df_reg_new, ", степени свободы ошибок =", df_error_new)
    print("MSE =", MSE_new)
    print("F статистика =", F_stat_new)
    print("Критическое F (при α = 0.05) =", F_crit_new)
    if F_stat_new > F_crit_new:
        print("Новая модель адекватна на уровне значимости α =", alpha)
    else:
        print("Новая модель неадекватна на уровне значимости α =", alpha)
else:
    print("Все факторы значимы. Селекция не требуется.")
