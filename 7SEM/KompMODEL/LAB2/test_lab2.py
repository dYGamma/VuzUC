import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def simulate_poisson_process(lam, T):
    times = []
    time = 0
    while time < T:
        time_to_next_event = np.random.exponential(1/lam)
        time += time_to_next_event
        if time < T:
            times.append(time)
    return np.array(times)

# Номер студента
N = 14

# Заданные параметры
T1 = N
T2 = N + 100
lambda1 = (N + 8) / (N + 24)
lambda2 = (N + 9) / (N + 25)

# Симуляция двух потоков
process1 = simulate_poisson_process(lambda1, T2 - T1)
process2 = simulate_poisson_process(lambda2, T2 - T1)

# Суммирование событий
combined_process = np.sort(np.concatenate([process1, process2]))

# Вычисляем интервалы времени для суммарного потока
intervals_combined = np.diff(combined_process)

# Теоретическое распределение для суммарного процесса
lam_sum = lambda1 + lambda2
expected_intervals = np.random.exponential(1 / lam_sum, len(intervals_combined))

# Тест Колмогорова-Смирнова
ks_stat, p_value = stats.ks_2samp(intervals_combined, expected_intervals)
print(f"KS Statistic: {ks_stat}, p-value: {p_value}")

# Визуализация
plt.step(np.concatenate([[T1], process1 + T1]), np.arange(len(process1) + 1), where='post', label=f'Poisson Process 1 (λ={lambda1:.2f})')
plt.step(np.concatenate([[T1], process2 + T1]), np.arange(len(process2) + 1), where='post', label=f'Poisson Process 2 (λ={lambda2:.2f})')
plt.step(np.concatenate([[T1], combined_process + T1]), np.arange(len(combined_process) + 1), where='post', label=f'Combined Process (λ={lam_sum:.2f})')
plt.xlabel('Time')
plt.ylabel('Number of Events')
plt.title('Simulation of Poisson Processes and Their Sum')
plt.legend()
plt.show()
