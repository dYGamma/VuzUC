import numpy as np
import scipy.stats as st

# Исходные данные
x = np.array([-1, 0, 1, 2, 3])
y = np.array([15, 12, 6, 1, -2])
n = len(x)

print("Исходные данные:")
print("x =", x)
print("y =", y)
print("Число наблюдений n =", n)
print("--------------------------------------------------")

# ===============================
# 1. Квадратичная модель: y = a0 + a1*x + a2*x^2
# ===============================

# Формирование дизайн-матрицы для квадратичной модели
X_quad = np.column_stack((np.ones(n), x, x**2))

# ----- Скалярный метод (составление нормальных уравнений) -----
# Вычисляем необходимые суммы:
sum_x   = np.sum(x)
sum_x2  = np.sum(x**2)
sum_x3  = np.sum(x**3)
sum_x4  = np.sum(x**4)
sum_y   = np.sum(y)
sum_xy  = np.sum(x*y)
sum_x2y = np.sum(x**2 * y)

# Система нормальных уравнений:
#    n*a0    + (sum_x)*a1    + (sum_x2)*a2 = sum_y
# (sum_x)*a0 + (sum_x2)*a1   + (sum_x3)*a2 = sum_xy
# (sum_x2)*a0+ (sum_x3)*a1   + (sum_x4)*a2 = sum_x2y
A = np.array([[n,      sum_x,   sum_x2],
              [sum_x,  sum_x2,  sum_x3],
              [sum_x2, sum_x3,  sum_x4]])
b_vec = np.array([sum_y, sum_xy, sum_x2y])

beta_scalar = np.linalg.solve(A, b_vec)
print("Коэффициенты (скалярный метод):")
print("a0 = {:.4f}, a1 = {:.4f}, a2 = {:.4f}".format(*beta_scalar))
print("--------------------------------------------------")

# ----- Матричный метод -----
# Решаем матричное уравнение: β = (XᵀX)⁻¹ · Xᵀy
beta_matrix = np.linalg.inv(X_quad.T @ X_quad) @ (X_quad.T @ y)
print("Коэффициенты (матричный метод):")
print("a0 = {:.4f}, a1 = {:.4f}, a2 = {:.4f}".format(*beta_matrix))
print("--------------------------------------------------")

# Вычисляем предсказанные значения и остатки
y_pred_quad = X_quad @ beta_matrix
residuals_quad = y - y_pred_quad

# Вычисляем общую сумму квадратов (SST), сумму квадратов ошибок (SSE) и сумму квадратов регрессии (SSR)
y_bar = np.mean(y)
SST = np.sum((y - y_bar)**2)
SSE = np.sum(residuals_quad**2)
SSR = SST - SSE

print("Для квадратичной модели:")
print("SST = {:.4f}".format(SST))
print("SSE = {:.4f}".format(SSE))
print("SSR = {:.4f}".format(SSR))

# Степени свободы
p_quad = 3  # число оцениваемых коэффициентов
df_reg = p_quad - 1       # регрессионные степени свободы
df_res = n - p_quad       # остатков

# Среднеквадратичные статистики
MSR = SSR / df_reg
MSE = SSE / df_res

# F-статистика для проверки адекватности модели по Фишеру
F_stat = MSR / MSE
p_value_F = 1 - st.f.cdf(F_stat, df_reg, df_res)
print("F-статистика (квадратичная модель) = {:.4f}, p-value = {:.4f}".format(F_stat, p_value_F))
print("--------------------------------------------------")

# ----- Проверка значимости коэффициентов (критерий Стьюдента) -----
# Оценка дисперсии коэффициентов: Var(β) = MSE * (XᵀX)⁻¹
XtX_inv = np.linalg.inv(X_quad.T @ X_quad)
var_beta = MSE * XtX_inv
se_beta = np.sqrt(np.diag(var_beta))  # стандартные ошибки

# t-статистика для каждого коэффициента
t_stats = beta_matrix / se_beta
p_values_t = 2 * (1 - st.t.cdf(np.abs(t_stats), df_res))

print("Коэффициенты, стандартные ошибки, t-статистика и p-value (квадратичная модель):")
for i, (coef, se, t_val, p_val) in enumerate(zip(beta_matrix, se_beta, t_stats, p_values_t)):
    print(f"a{i} = {coef:8.4f}, se = {se:6.4f}, t = {t_val:6.4f}, p = {p_val:8.4f}")

# Критическое значение t при уровне значимости α = 0,01 (двусторонний тест)
alpha = 0.01
t_crit = st.t.ppf(1 - alpha/2, df_res)
print("Критическое значение t при α = {:.2f} и df = {}: {:.4f}".format(alpha, df_res, t_crit))
print("--------------------------------------------------")

# Если какой-либо коэффициент незначим (например, a2), исключаем его и переоцениваем модель.
if np.abs(t_stats[2]) < t_crit:
    print("Коэффициент a2 (при x^2) незначим (|t| = {:.4f} < t_crit = {:.4f}).".format(np.abs(t_stats[2]), t_crit))
    print("Переоцениваем модель, исключая член x^2 (линейная регрессия).")
    
    # ===============================
    # 2. Линейная модель: y = b0 + b1*x
    # ===============================
    X_lin = np.column_stack((np.ones(n), x))
    beta_lin = np.linalg.inv(X_lin.T @ X_lin) @ (X_lin.T @ y)
    
    print("Коэффициенты линейной модели:")
    print("b0 = {:.4f}, b1 = {:.4f}".format(*beta_lin))
    
    # Предсказания и остатки для линейной модели
    y_pred_lin = X_lin @ beta_lin
    residuals_lin = y - y_pred_lin
    SSE_lin = np.sum(residuals_lin**2)
    SSR_lin = SST - SSE_lin
    
    # Степени свободы для линейной модели
    p_lin = 2
    df_reg_lin = p_lin - 1
    df_res_lin = n - p_lin
    
    MSR_lin = SSR_lin / df_reg_lin
    MSE_lin = SSE_lin / df_res_lin
    
    # F-статистика для линейной модели
    F_stat_lin = MSR_lin / MSE_lin
    p_value_F_lin = 1 - st.f.cdf(F_stat_lin, df_reg_lin, df_res_lin)
    
    print("Для линейной модели:")
    print("SSE = {:.4f}".format(SSE_lin))
    print("SSR = {:.4f}".format(SSR_lin))
    print("F-статистика = {:.4f}, p-value = {:.4f}".format(F_stat_lin, p_value_F_lin))
    if p_value_F_lin < alpha:
        print("Линейная модель является адекватной (p-value < α).")
    else:
        print("Линейная модель не является адекватной (p-value ≥ α).")
    print("--------------------------------------------------")
    
    # Проверка значимости коэффициентов линейной модели
    XtX_inv_lin = np.linalg.inv(X_lin.T @ X_lin)
    var_beta_lin = MSE_lin * XtX_inv_lin
    se_beta_lin = np.sqrt(np.diag(var_beta_lin))
    t_stats_lin = beta_lin / se_beta_lin
    p_values_t_lin = 2 * (1 - st.t.cdf(np.abs(t_stats_lin), df_res_lin))
    
    print("Коэффициенты, стандартные ошибки, t-статистика и p-value (линейная модель):")
    for i, (coef, se, t_val, p_val) in enumerate(zip(beta_lin, se_beta_lin, t_stats_lin, p_values_t_lin)):
        print(f"b{i} = {coef:8.4f}, se = {se:6.4f}, t = {t_val:6.4f}, p = {p_val:8.4f}")
    
    # Проверка t-критерия для линейной модели
    t_crit_lin = st.t.ppf(1 - alpha/2, df_res_lin)
    print("Критическое значение t для линейной модели при α = {:.2f} и df = {}: {:.4f}".format(alpha, df_res_lin, t_crit_lin))
else:
    print("Все коэффициенты квадратичной модели значимы, повторная оценка не требуется.")

