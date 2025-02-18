import streamlit as st
import numpy as np
import scipy.stats as st_stats
import matplotlib.pyplot as plt

# Заголовок приложения
st.title("Анализ регрессии: Квадратичная и Линейная модели")
st.write("""
Это приложение выполняет анализ данных с использованием квадратичной и линейной моделей.
Оно вычисляет коэффициенты, остатки, F-статистику и проверяет значимость коэффициентов.
""")

# Исходные данные
x = np.array([-1, 0, 1, 2, 3])
y = np.array([15, 12, 6, 1, -2])

# Пользовательский ввод
st.sidebar.header("Параметры")
custom_data = st.sidebar.checkbox("Использовать собственные данные?")
if custom_data:
    x_input = st.sidebar.text_input("Введите значения x (через запятую)", "-1,0,1,2,3")
    y_input = st.sidebar.text_input("Введите значения y (через запятую)", "15,12,6,1,-2")
    try:
        x = np.array([float(i) for i in x_input.split(",")])
        y = np.array([float(i) for i in y_input.split(",")])
    except ValueError:
        st.error("Ошибка ввода данных. Пожалуйста, введите числа через запятую.")
        st.stop()

n = len(x)

# Отображение исходных данных
st.subheader("Исходные данные")
data = {"x": x, "y": y}
st.table(data)
st.write(f"Число наблюдений n = {n}")

# ===============================
# 1. Квадратичная модель: y = a0 + a1*x + a2*x^2
# ===============================
st.subheader("Квадратичная модель")
X_quad = np.column_stack((np.ones(n), x, x**2))

# Скалярный метод
sum_x = np.sum(x)
sum_x2 = np.sum(x**2)
sum_x3 = np.sum(x**3)
sum_x4 = np.sum(x**4)
sum_y = np.sum(y)
sum_xy = np.sum(x * y)
sum_x2y = np.sum(x**2 * y)

A = np.array([[n, sum_x, sum_x2],
              [sum_x, sum_x2, sum_x3],
              [sum_x2, sum_x3, sum_x4]])
b_vec = np.array([sum_y, sum_xy, sum_x2y])
beta_scalar = np.linalg.solve(A, b_vec)

st.write("Коэффициенты (скалярный метод):")
st.write(f"a0 = {beta_scalar[0]:.4f}, a1 = {beta_scalar[1]:.4f}, a2 = {beta_scalar[2]:.4f}")

# Матричный метод
beta_matrix = np.linalg.inv(X_quad.T @ X_quad) @ (X_quad.T @ y)
st.write("Коэффициенты (матричный метод):")
st.write(f"a0 = {beta_matrix[0]:.4f}, a1 = {beta_matrix[1]:.4f}, a2 = {beta_matrix[2]:.4f}")

# Предсказанные значения и остатки
y_pred_quad = X_quad @ beta_matrix
residuals_quad = y - y_pred_quad
y_bar = np.mean(y)
SST = np.sum((y - y_bar)**2)
SSE = np.sum(residuals_quad**2)
SSR = SST - SSE

st.write("Для квадратичной модели:")
st.write(f"SST = {SST:.4f}, SSE = {SSE:.4f}, SSR = {SSR:.4f}")

# F-статистика
p_quad = 3
df_reg = p_quad - 1
df_res = n - p_quad
MSR = SSR / df_reg
MSE = SSE / df_res
F_stat = MSR / MSE
p_value_F = 1 - st_stats.f.cdf(F_stat, df_reg, df_res)
st.write(f"F-статистика = {F_stat:.4f}, p-value = {p_value_F:.4f}")

# График квадратичной модели
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color="blue", label="Исходные данные")
plt.plot(x, y_pred_quad, color="red", label="Квадратичная модель")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
st.pyplot(plt)

# Проверка значимости коэффициентов
XtX_inv = np.linalg.inv(X_quad.T @ X_quad)
var_beta = MSE * XtX_inv
se_beta = np.sqrt(np.diag(var_beta))
t_stats = beta_matrix / se_beta
p_values_t = 2 * (1 - st_stats.t.cdf(np.abs(t_stats), df_res))

st.write("Коэффициенты, стандартные ошибки, t-статистика и p-value (квадратичная модель):")
for i, (coef, se, t_val, p_val) in enumerate(zip(beta_matrix, se_beta, t_stats, p_values_t)):
    st.write(f"a{i} = {coef:.4f}, se = {se:.4f}, t = {t_val:.4f}, p = {p_val:.4f}")

alpha = 0.01
t_crit = st_stats.t.ppf(1 - alpha/2, df_res)
st.write(f"Критическое значение t при α = {alpha:.2f} и df = {df_res}: {t_crit:.4f}")

# Переоценка модели, если a2 незначим
if np.abs(t_stats[2]) < t_crit:
    st.write("Коэффициент a2 (при x^2) незначим. Переоцениваем модель, исключая член x^2 (линейная регрессия).")
    
    # ===============================
    # 2. Линейная модель: y = b0 + b1*x
    # ===============================
    X_lin = np.column_stack((np.ones(n), x))
    beta_lin = np.linalg.inv(X_lin.T @ X_lin) @ (X_lin.T @ y)
    st.write("Коэффициенты линейной модели:")
    st.write(f"b0 = {beta_lin[0]:.4f}, b1 = {beta_lin[1]:.4f}")
    
    # Предсказания и остатки для линейной модели
    y_pred_lin = X_lin @ beta_lin
    residuals_lin = y - y_pred_lin
    SSE_lin = np.sum(residuals_lin**2)
    SSR_lin = SST - SSE_lin
    
    # F-статистика для линейной модели
    p_lin = 2
    df_reg_lin = p_lin - 1
    df_res_lin = n - p_lin
    MSR_lin = SSR_lin / df_reg_lin
    MSE_lin = SSE_lin / df_res_lin
    F_stat_lin = MSR_lin / MSE_lin
    p_value_F_lin = 1 - st_stats.f.cdf(F_stat_lin, df_reg_lin, df_res_lin)
    
    st.write("Для линейной модели:")
    st.write(f"SSE = {SSE_lin:.4f}, SSR = {SSR_lin:.4f}")
    st.write(f"F-статистика = {F_stat_lin:.4f}, p-value = {p_value_F_lin:.4f}")
    if p_value_F_lin < alpha:
        st.write("Линейная модель является адекватной (p-value < α).")
    else:
        st.write("Линейная модель не является адекватной (p-value ≥ α).")
    
    # График линейной модели
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", label="Исходные данные")
    plt.plot(x, y_pred_lin, color="green", label="Линейная модель")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    st.pyplot(plt)
else:
    st.write("Все коэффициенты квадратичной модели значимы, повторная оценка не требуется.")