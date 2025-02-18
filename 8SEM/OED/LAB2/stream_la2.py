import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
import streamlit as st

# Заголовок приложения
st.title("Анализ статистического распределения")

# Ввод данных через интерфейс Streamlit
st.sidebar.header("Ввод данных")
intervals_input = st.sidebar.text_area(
    "Введите интервалы (через запятую, например: -0.3,-0.2; -0.2,-0.1; ...)",
    "-0.3,-0.2; -0.2,-0.1; -0.1,0; 0,0.1; 0.1,0.2; 0.2,0.3; 0.3,0.4"
)
m_i_input = st.sidebar.text_input(
    "Введите частоты (через запятую, например: 2,14,25,27,17,11,4)",
    "2,14,25,27,17,11,4"
)

# Преобразование ввода в списки
try:
    intervals = [tuple(map(float, pair.split(','))) for pair in intervals_input.split(';')]
    m_i = list(map(int, m_i_input.split(',')))
    n = sum(m_i)  # Общее количество наблюдений
except Exception as e:
    st.error(f"Ошибка ввода данных: {e}")
    st.stop()

# Шаг 1: Статистические вероятности
p_i = [m / n for m in m_i]

# Шаг 2: Плотности вероятности для гистограммы
delta_x = intervals[0][1] - intervals[0][0]  # Длина интервала
f_i = [p / delta_x for p in p_i]

# Середины интервалов
midpoints = [(a + b) / 2 for a, b in intervals]

# Построение гистограммы
fig, ax = plt.subplots()
ax.bar(midpoints, f_i, width=delta_x, alpha=0.6, color='blue', edgecolor='black', label='Экспериментальная гистограмма')

# Шаг 3: Теоретическая плотность нормального распределения
mu = sum(mid * m for mid, m in zip(midpoints, m_i)) / n
sigma_squared = sum(((mid - mu) ** 2) * m for mid, m in zip(midpoints, m_i)) / n
sigma = np.sqrt(sigma_squared)

# Теоретическая плотность нормального распределения
x_theory = np.linspace(min(midpoints) - delta_x, max(midpoints) + delta_x, 500)
f_theory = norm.pdf(x_theory, loc=mu, scale=sigma)

# Добавление теоретической кривой на график
ax.plot(x_theory, f_theory, color='red', linewidth=2, label='Теоретическая плотность')

# Настройка графика
ax.set_title("Гистограмма и теоретическая плотность")
ax.set_xlabel("Значения случайной величины")
ax.set_ylabel("Плотность вероятности")
ax.legend()
ax.grid()

# Отображение графика в Streamlit
st.pyplot(fig)

# Вывод параметров распределения
st.subheader("Параметры распределения")
st.write(f"Математическое ожидание (μ): {mu:.4f}")
st.write(f"Стандартное отклонение (σ): {sigma:.4f}")

# Шаг 4: Проверка гипотезы о нормальном распределении (критерий хи-квадрат)
theoretical_probabilities = [
    norm.cdf(b, loc=mu, scale=sigma) - norm.cdf(a, loc=mu, scale=sigma) for a, b in intervals
]
theoretical_frequencies = [p * n for p in theoretical_probabilities]

# Статистика хи-квадрат
chi2_stat = sum(((m - n_theor) ** 2) / n_theor for m, n_theor in zip(m_i, theoretical_frequencies))
degrees_of_freedom = len(intervals) - 1 - 2  # k = n - 1 - r (r = 2 для нормального распределения)
alpha = 0.025  # Уровень значимости для четных вариантов
chi2_critical = chi2.ppf(1 - alpha, degrees_of_freedom)

# Вывод результатов проверки гипотезы
st.subheader("Проверка гипотезы о нормальном распределении")
st.write(f"Статистика хи-квадрат: {chi2_stat:.4f}")
st.write(f"Критическое значение хи-квадрат: {chi2_critical:.4f}")

if chi2_stat < chi2_critical:
    st.success("Гипотеза о нормальном распределении принимается.")
else:
    st.error("Гипотеза о нормальном распределении отвергается.")