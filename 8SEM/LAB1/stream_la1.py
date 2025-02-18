import math
from scipy.stats import norm
import streamlit as st

# Заголовок приложения
st.title("Анализ данных с использованием доверительных интервалов")

# Ввод данных пользователем
st.header("Введите данные")
data_input = st.text_input(
    "Массив экспериментальных данных (через запятую):",
    "0.1, 0.4, 0.6, 2.9, 2, 1.2, 0.7, 1.7, 2.1, 7.1, 6.5, 19.2"
)
confidence_level = st.slider(
    "Доверительная вероятность (β)", 
    min_value=0.5, max_value=0.99, value=0.95, step=0.01
)
epsilon_beta = st.number_input(
    "Максимальная вероятная погрешность (εβ)", 
    min_value=0.01, value=0.38, step=0.01
)

# Преобразуем введенные данные в массив чисел
try:
    arr = [float(x.strip()) for x in data_input.split(",")]
except ValueError:
    st.error("Ошибка: Пожалуйста, введите корректные числовые данные через запятую.")
    st.stop()

# 1. Оценка математического ожидания
avg = sum(arr) / len(arr)
st.write("Математическое ожидание:", avg)

# 2. Выборочное стандартное отклонение
std = math.sqrt(sum((x - avg)**2 for x in arr) / (len(arr) - 1))
st.write("Выборочное стандартное отклонение:", std)

# 3. Построение доверительного интервала для заданной доверительной вероятности
n = len(arr)
z_score_confidence = norm.ppf(1 - (1 - confidence_level) / 2)  # Z-значение для β
margin_of_error = z_score_confidence * (std / math.sqrt(n))
confidence_interval = [avg - margin_of_error, avg + margin_of_error]
st.write(f"{confidence_level * 100:.0f}%-й доверительный интервал:", confidence_interval)

# 4. Отсеивание аномальных значений
filtered_values = [x for x in arr if confidence_interval[0] <= x <= confidence_interval[1]]
if len(filtered_values) < len(arr):
    st.write("Аномальные значения:", set(arr) - set(filtered_values))
else:
    st.write("Аномальных значений не найдено")

# 5. Уточнённая оценка математического ожидания
filtered_avg = sum(filtered_values) / len(filtered_values)
st.write("Уточнённое математическое ожидание:", filtered_avg)

# 6a. Доверительный интервал для уточнённого математического ожидания
filtered_std = math.sqrt(sum((x - filtered_avg)**2 for x in filtered_values) / (len(filtered_values) - 1))
n_filtered = len(filtered_values)
z_score_filtered = norm.ppf(1 - (1 - confidence_level) / 2)
quality_error = z_score_filtered * (filtered_std / math.sqrt(n_filtered))
interval_filtered = [filtered_avg - quality_error, filtered_avg + quality_error]
st.write("Доверительный интервал для уточнённого матожидания:", interval_filtered)

# 6b. Доверительная вероятность для заданной максимальной вероятной погрешности
z_score_epsilon = (epsilon_beta * math.sqrt(n_filtered)) / filtered_std
p_confidence = norm.cdf(z_score_epsilon) - norm.cdf(-z_score_epsilon)
st.write(f"Доверительная вероятность для погрешности {epsilon_beta}: {p_confidence:.4f}")