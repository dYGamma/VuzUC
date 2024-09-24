import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, poisson, kstest, chisquare

# Функция для генерации пуассоновских потоков
def generate_poisson_process(lmbda, T, size=50):
    inter_arrival_times = -np.log(np.random.rand(size)) / lmbda
    event_times = np.cumsum(inter_arrival_times)
    return event_times[event_times <= T]

# Функция для построения графиков
def plot_processes(lmbda1, lmbda2, T, num_realizations=100):
    plt.figure(figsize=(12, 6))

    # Генерация пуассоновских потоков
    events1 = [generate_poisson_process(lmbda1, T) for _ in range(num_realizations)]
    events2 = [generate_poisson_process(lmbda2, T) for _ in range(num_realizations)]
    
    # Суммируем два пуассоновских потока
    sum_events = [np.sort(np.concatenate([e1, e2])) for e1, e2 in zip(events1, events2)]

    # Построение графиков потоков
    plt.subplot(1, 3, 1)
    for e in events1:
        plt.step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    plt.title(f'Poisson Process λ1={lmbda1}')
    
    plt.subplot(1, 3, 2)
    for e in events2:
        plt.step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    plt.title(f'Poisson Process λ2={lmbda2}')
    
    plt.subplot(1, 3, 3)
    for e in sum_events:
        plt.step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    plt.title('Summed Poisson Process')

    plt.tight_layout()
    plt.show()

    return events1, events2, sum_events

# Функция для расчета статистических характеристик
def compute_statistics(events, lmbda, T):
    counts = np.array([len(e) for e in events])
    
    # Вычисление теоретических и эмпирических параметров
    empirical_lambda = np.mean(counts) / T
    empirical_var = np.var(counts)
    theoretical_var = lmbda * T

    # KS-тест
    inter_arrival_times = np.concatenate([np.diff(e) for e in events if len(e) > 1])
    ks_stat, ks_pvalue = kstest(inter_arrival_times, 'expon', args=(0, 1/lmbda))
    
    # χ²-тест
    max_count = max(counts)  # максимальное количество событий
    expected_counts = poisson(lmbda * T).pmf(np.arange(0, max_count + 1)) * len(events)
    
    # Приведение массивов к одинаковой длине
    observed_counts = np.bincount(counts, minlength=len(expected_counts))
    expected_counts = expected_counts[:len(observed_counts)]  # Обрезаем по длине наблюдаемых значений
    
    # Нормализация: делаем суммы наблюдаемых и ожидаемых частот равными
    expected_counts *= observed_counts.sum() / expected_counts.sum()

    chi2_stat, chi2_pvalue = chisquare(observed_counts, f_exp=expected_counts)

    return {
        'empirical_lambda': empirical_lambda,
        'theoretical_var': theoretical_var,
        'empirical_var': empirical_var,
        'ks_stat': ks_stat,
        'ks_pvalue': ks_pvalue,
        'chi2_stat': chi2_stat,
        'chi2_pvalue': chi2_pvalue
    }

# Основная функция
def main():
    T = 10  # Время наблюдения
    num_realizations = 100  # Количество реализаций для увеличенной точности

    # Параметры потоков
    lmbda1 = 3  # Интенсивность первого потока
    lmbda2 = 2  # Интенсивность второго потока

    # Визуализация потоков
    events1, events2, sum_events = plot_processes(lmbda1, lmbda2, T, num_realizations)

    # Расчет статистических характеристик для каждого потока
    stats1 = compute_statistics(events1, lmbda1, T)
    stats2 = compute_statistics(events2, lmbda2, T)
    stats_sum = compute_statistics(sum_events, lmbda1 + lmbda2, T)

    # Вывод результатов
    print(f"Stats for Process λ1={lmbda1}: {stats1}")
    print(f"Stats for Process λ2={lmbda2}: {stats2}")
    print(f"Stats for Summed Process (λ1 + λ2): {stats_sum}")

if __name__ == "__main__":
    main()
