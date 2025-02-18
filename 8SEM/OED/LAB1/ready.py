import math
from scipy.stats import norm

# Данные
arr = [0.1, 0.4, 0.6, 2.9, 2, 1.2, 0.7, 1.7, 2.1, 7.1, 6.5, 19.2]

# 1. Оценка математического ожидания
avg = sum(arr) / len(arr)
print("Математическое ожидание:", avg)

# 2. Выборочное стандартное отклонение
std = math.sqrt(sum((x - avg)**2 for x in arr) / (len(arr) - 1))
print("Выборочное стандартное отклонение:", std)

# 3. Построение 95%-го доверительного интервала
n = len(arr)
z_95 = 1.96
margin_of_error_95 = z_95 * (std / math.sqrt(n))
dov_int_95 = [avg - margin_of_error_95, avg + margin_of_error_95]
print("95%-й доверительный интервал:", dov_int_95)

# 4. Отсеивание аномальных значений
filtered_values = [x for x in arr if dov_int_95[0] <= x <= dov_int_95[1]]
if len(filtered_values) < len(arr):
    print("Аномальные значения:", set(arr) - set(filtered_values))
else:
    print("Аномальных значений не найдено")

# 5. Уточнённая оценка математического ожидания
filtered_avg = sum(filtered_values) / len(filtered_values)
print("Уточнённое математическое ожидание:", filtered_avg)

# 6a. Доверительный интервал для уточнённого математического ожидания
filtered_std = math.sqrt(sum((x - filtered_avg)**2 for x in filtered_values) / (len(filtered_values) - 1))
n_filtered = len(filtered_values)
z_92 = 1.75
quality_error = z_92 * (filtered_std / math.sqrt(n_filtered))
interval_92 = [filtered_avg - quality_error, filtered_avg + quality_error]
print("Доверительный интервал для уточнённого матожидания:", interval_92)

# 6b. Доверительная вероятность для заданной максимальной вероятной погрешности
epsilon = 0.38
z_score = (epsilon * math.sqrt(n_filtered)) / filtered_std
p_confidence = norm.cdf(z_score) - norm.cdf(-z_score)
print(f"Доверительная вероятность для погрешности {epsilon}: {p_confidence:.4f}")