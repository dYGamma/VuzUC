import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chisquare, poisson

def generate_poisson_process(lmbda, T):
    T0 = 0
    events = []

    while True:
        xi = np.random.rand()
        t_i = -np.log(xi) / lmbda

        if len(events) == 0:
            T_j = T0 + t_i
        else:
            T_j = events[-1] + t_i

        if T_j > T:
            break

        events.append(T_j)
    return events

# Исходные данные
N = 19
T1 = N
T2 = N + 100
lam1 = (N + 8) / (N + 24)
lam2 = (N + 9) / (N + 25)
T = T2 - T1

# Параметры симуляции
num_simulations = 40
num_intervals = 25

# Переменные для подсчета результатов
confirmed_count = 0
rejected_count = 0

# Многократный запуск симуляции
for sim in range(num_simulations):
    # Генерация пуассоновских процессов
    poisson_events1 = generate_poisson_process(lam1, T)
    poisson_events2 = generate_poisson_process(lam2, T)
    sum_events = np.sort(np.concatenate((poisson_events1, poisson_events2)))

    # Статистическая обработка данных
    interval_length = T / num_intervals
    observed_counts = []

    for i in range(num_intervals):
        start = i * interval_length
        end = (i + 1) * interval_length
        count = np.sum((sum_events >= start) & (sum_events < end))
        observed_counts.append(count)

    # Преобразуем список в массив numpy
    observed_counts = np.array(observed_counts)

    # Расчет ожидаемых частот
    lambda_sum = lam1 + lam2
    expected_counts = [lambda_sum * interval_length] * num_intervals

    # Нормализация ожидаемых значений, чтобы их сумма совпадала с суммой наблюдаемых значений
    total_observed = np.sum(observed_counts)
    total_expected = np.sum(expected_counts)

    # Масштабируем ожидаемые значения
    expected_counts = [count * (total_observed / total_expected) for count in expected_counts]

    # Проверка гипотезы с помощью критерия хи-квадрат
    chi2_stat, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts)

    # Подсчет подтвержденных и отвергнутых гипотез
    if p_value > 0.05:
        confirmed_count += 1
        hypothesis_result = "Гипотеза о пуассоновости суммарного потока не отвергается."
    else:
        rejected_count += 1
        hypothesis_result = "Гипотеза о пуассоновости суммарного потока отвергается."

# Визуализация процессов для последнего запуска
plt.figure(figsize=(10, 8))

# График 1: Первый пуассоновский процесс
plt.subplot(311)
plt.scatter(poisson_events1, y=[0] * len(poisson_events1), color='b')
plt.title('Пуассоновский процесс 1')
plt.xlim(0, T)
plt.xlabel('Время')
plt.ylabel('События')

# График 2: Второй пуассоновский процесс
plt.subplot(312)
plt.scatter(poisson_events2, y=[0] * len(poisson_events2), color='r')
plt.title('Пуассоновский процесс 2')
plt.xlim(0, T)
plt.xlabel('Время')
plt.ylabel('События')

# Наложенный график
plt.subplot(313)
plt.scatter(poisson_events1, y=[0] * len(poisson_events1), alpha=0.5, color='b', label='Процесс 1')
plt.scatter(poisson_events2, y=[0] * len(poisson_events2), alpha=0.5, color='r', label='Процесс 2')
plt.title('Наложенные пуассоновские процессы')
plt.xlim(0, T)
plt.xlabel('Время')
plt.ylabel('События')
plt.legend()

plt.tight_layout()
plt.show()

# Вывод результатов последнего запуска
print("\n=== Результаты последнего запуска ===")
print(f"Теоретические lam1 и lam2: ({lam1:.4f}, {lam2:.4f})")
print(f"Практические lam1 и lam2: ({len(poisson_events1) / T:.4f}, {len(poisson_events2) / T:.4f})")
print(f"Значение статистики хи-квадрат: {chi2_stat:.4f}")
print(f"Значение p-value: {p_value:.4f}")
print(hypothesis_result)

# Вывод сводной статистики по всем запускам
print(f"\n=== Сводная статистика по {num_simulations} запускам ===")
print(f"Количество подтверждений гипотезы: {confirmed_count}")
print(f"Количество отвергнутых гипотез: {rejected_count}")