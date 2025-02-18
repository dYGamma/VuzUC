import numpy as np
import scipy.stats as stats
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

# Настройка страницы Streamlit
st.set_page_config(
    page_title="Множественная регрессия",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стиль для графиков
style.use("seaborn-v0_8-darkgrid")

# Заголовок с иконкой
st.markdown("""
<h1 style="text-align: center; color: #4CAF50;">
    📊 Анализ множественной регрессии
</h1>
<p style="text-align: center; font-size: 16px; color: #555;">
    Этот инструмент выполняет анализ множественной регрессии на основе предоставленных данных.
</p>
""", unsafe_allow_html=True)

# Исходные данные по умолчанию
default_data = {
    "x1": [2, 3, 4, 6, 7, -1],
    "x2": [-2, 0, 1, 2, 3, -1],
    "y": [16, 6, 1, -2, -8, 7]
}

# Боковая панель для редактирования данных
with st.sidebar:
    st.markdown("""
    <h2 style="color: #FF9800;">📝 Редактирование данных</h2>
    """, unsafe_allow_html=True)
    st.markdown("Введите новые значения для `x1`, `x2` и `y`. Каждое значение должно быть разделено запятой.")
    x1_input = st.text_input("x1 (через запятую)", value=",".join(map(str, default_data["x1"])))
    x2_input = st.text_input("x2 (через запятую)", value=",".join(map(str, default_data["x2"])))
    y_input = st.text_input("y (через запятую)", value=",".join(map(str, default_data["y"])))

# Преобразование ввода в массивы NumPy
try:
    x1 = np.array(list(map(float, x1_input.split(","))))
    x2 = np.array(list(map(float, x2_input.split(","))))
    y = np.array(list(map(float, y_input.split(","))))

    if len(x1) != len(x2) or len(x1) != len(y):
        st.error("Ошибка: Длины массивов x1, x2 и y должны совпадать!")
        st.stop()

except ValueError:
    st.error("Ошибка: Введите числовые значения, разделенные запятыми!")
    st.stop()

# Главная область: Отображение текущих данных
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <h3 style="color: #2196F3;">📋 Текущие данные</h3>
    """, unsafe_allow_html=True)
    data = pd.DataFrame({"x1": x1, "x2": x2, "y": y})
    st.dataframe(data.style.highlight_max(axis=0, color="#876c99"))

with col2:
    st.markdown("""
    <h3 style="color: #9C27B0;">📊 Основные статистики</h3>
    """, unsafe_allow_html=True)
    stats_data = pd.DataFrame({
        "Параметр": ["Среднее", "Минимум", "Максимум"],
        "x1": [np.mean(x1), np.min(x1), np.max(x1)],
        "x2": [np.mean(x2), np.min(x2), np.max(x2)],
        "y": [np.mean(y), np.min(y), np.max(y)]
    })

    styled_stats_data = stats_data.style.format({
        "x1": "{:.2f}",
        "x2": "{:.2f}",
        "y": "{:.2f}"
    }).set_table_styles([
        {"selector": "th", "props": [("background-color", "#E3F2FD"), ("color", "#333")]}
    ])

    st.dataframe(styled_stats_data)

# Центрирование факторов
mean_x1 = np.mean(x1)
mean_x2 = np.mean(x2)
x1_centered = x1 - mean_x1
x2_centered = x2 - mean_x2

st.markdown("""
<hr style="border: 1px solid #ddd;">
<h3 style="color: #F44336;">🎯 Центрированные факторы</h3>
""", unsafe_allow_html=True)
centered_data = pd.DataFrame({"x1_centered": x1_centered, "x2_centered": x2_centered})
st.dataframe(centered_data.style.bar(color="#FF9800"))

# Построение модели
n = len(y)
X = np.column_stack((np.ones(n), x1_centered, x2_centered))
k = 2  # число факторов

XtX = X.T @ X
XtX_inv = np.linalg.inv(XtX)
beta_hat = XtX_inv @ (X.T @ y)

st.markdown("""
<hr style="border: 1px solid #ddd;">
<h3 style="color: #03A9F4;">📈 Оценки коэффициентов регрессии</h3>
""", unsafe_allow_html=True)
coefficients = pd.DataFrame({
    "Коэффициент": ["beta0 (интерсепт)", "beta1", "beta2"],
    "Значение": beta_hat
})

styled_coefficients = coefficients.style.map(
    lambda x: "background-color: #C8E6C9; color: #333;" if isinstance(x, (int, float)) and abs(x) > 1 else "",
    subset=["Значение"]
)

st.dataframe(styled_coefficients)

# Уравнение регрессии
equation = f"y = {beta_hat[0]:.4f} + {beta_hat[1]:.4f}*(x1 - {mean_x1:.4f}) + {beta_hat[2]:.4f}*(x2 - {mean_x2:.4f})"
st.markdown(f"<h4 style='color: #795548;'>📝 Уравнение регрессии:</h4><p style='font-size: 18px; color: #555;'>{equation}</p>", unsafe_allow_html=True)

# График наблюдений и предсказаний
st.markdown("""
<hr style="border: 1px solid #ddd;">
<h3 style="color: #673AB7;">📉 График наблюдений и предсказаний</h3>
""", unsafe_allow_html=True)
y_pred = X @ beta_hat
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(range(len(y)), y, label="Наблюдения", color="#2196F3", s=100)
ax.plot(range(len(y)), y_pred, label="Предсказания", color="#FF9800", linestyle="--", linewidth=3)
ax.set_xlabel("Номер наблюдения", fontsize=14)
ax.set_ylabel("Значение y", fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, linestyle="--", alpha=0.7)
st.pyplot(fig)

# Проверка адекватности модели
st.markdown("""
<hr style="border: 1px solid #ddd;">
<h3 style="color: #FF5722;">🔍 Проверка адекватности модели</h3>
""", unsafe_allow_html=True)
residuals = y - y_pred
RSS = np.sum(residuals**2)
TSS = np.sum((y - np.mean(y))**2)
ESS = TSS - RSS
df_reg = k
df_error = n - (k + 1)
MSE = RSS / df_error
F_stat = (ESS / df_reg) / MSE
alpha = 0.05
F_crit = stats.f.ppf(1 - alpha, df_reg, df_error)

fisher_results = pd.DataFrame({
    "Параметр": ["RSS", "TSS", "ESS", "Степени свободы регрессии", "Степени свободы ошибок", "MSE", "F статистика", "Критическое F"],
    "Значение": [RSS, TSS, ESS, df_reg, df_error, MSE, F_stat, F_crit]
})

styled_fisher_results = fisher_results.style.format({
    "Значение": "{:.4f}"  # Форматируем только числовой столбец
}).set_table_styles([
    {"selector": "th", "props": [("background-color", "#FFF3E0"), ("color", "#333")]}
])

st.dataframe(styled_fisher_results)

if F_stat > F_crit:
    st.success("✅ Модель адекватна на уровне значимости α = 0.05")
else:
    st.error("❌ Модель неадекватна на уровне значимости α = 0.05")

# Проверка значимости факторов
st.markdown("""
<hr style="border: 1px solid #ddd;">
<h3 style="color: #00BCD4;">📊 Проверка значимости факторов</h3>
""", unsafe_allow_html=True)

SE_beta = np.sqrt(np.diag(MSE * XtX_inv))
t_stats = beta_hat / SE_beta
p_values = [2 * (1 - stats.t.cdf(np.abs(t), df=df_error)) for t in t_stats]

student_results = pd.DataFrame({
    "Коэффициент": ["beta0 (интерсепт)", "beta1", "beta2"],
    "Стандартная ошибка": SE_beta,
    "t-статистика": t_stats,
    "p-value": p_values
})

# Применяем форматирование только к числовым столбцам
styled_student_results = (
    student_results.style
    .format({
        "Стандартная ошибка": "{:.4f}",
        "t-статистика": "{:.4f}",
        "p-value": "{:.4f}"
    })
    .map(
        lambda x: "background-color: #FFEBEE; color: #D32F2F;" 
                  if isinstance(x, (int, float)) and x > 0.05 else "",
        subset=["Стандартная ошибка", "t-статистика", "p-value"]  # Применяем только к числовым столбцам
    )
)

st.dataframe(styled_student_results)

insignificant = []
for i, p in enumerate(p_values):
    if p > alpha and i > 0:  # Пропускаем интерсепт
        insignificant.append(i)

if insignificant:
    st.warning(f"⚠️ Незначимые факторы (индексы коэффициентов): {insignificant}")
else:
    st.success("✅ Все факторы значимы. Селекция не требуется.")

# Селекция факторов
if insignificant:
    cols = [0] + [i for i in range(1, len(beta_hat)) if i not in insignificant]
    X_new = X[:, cols]
    XtX_new = X_new.T @ X_new
    XtX_inv_new = np.linalg.inv(XtX_new)
    beta_hat_new = XtX_inv_new @ (X_new.T @ y)

    st.subheader("Новая модель после исключения незначимых факторов")
    new_coefficients = pd.DataFrame({
        "Коэффициент": [f"beta{i}" for i in cols],
        "Значение": beta_hat_new
    })
    st.dataframe(new_coefficients)

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

    fisher_results_new = pd.DataFrame({
        "Параметр": ["RSS", "TSS", "ESS", "Степени свободы регрессии", "Степени свободы ошибок", "MSE", "F статистика", "Критическое F"],
        "Значение": [RSS_new, TSS_new, ESS_new, df_reg_new, df_error_new, MSE_new, F_stat_new, F_crit_new]
    })
    st.dataframe(fisher_results_new)

    if F_stat_new > F_crit_new:
        st.success("✅ Новая модель адекватна на уровне значимости α = 0.05")
    else:
        st.error("❌ Новая модель неадекватна на уровне значимости α = 0.05")