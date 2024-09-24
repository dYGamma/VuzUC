import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, poisson, kstest, chisquare
import streamlit as st

# Функция для генерации пуассоновских потоков
def generate_poisson_process(lmbda, T, size=500):
    inter_arrival_times = -np.log(np.random.rand(size)) / lmbda
    event_times = np.cumsum(inter_arrival_times)
    return event_times[event_times <= T]

# Функция для построения графиков
def plot_processes(lmbda1, lmbda2, T, num_realizations=50):
    fig, ax = plt.subplots(1, 3, figsize=(12, 6))

    # Генерация пуассоновских потоков
    events1 = [generate_poisson_process(lmbda1, T) for _ in range(num_realizations)]
    events2 = [generate_poisson_process(lmbda2, T) for _ in range(num_realizations)]
    
    # Суммируем два пуассоновских потока
    sum_events = [np.sort(np.concatenate([e1, e2])) for e1, e2 in zip(events1, events2)]

    # Построение графиков потоков
    for e in events1:
        ax[0].step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    ax[0].set_title(f'Пуас-ский поток λ1={lmbda1}')

    for e in events2:
        ax[1].step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    ax[1].set_title(f'Пуас-ский поток λ2={lmbda2}')
    
    for e in sum_events:
        ax[2].step(e, np.arange(1, len(e) + 1), where='post', alpha=0.3)
    ax[2].set_title('Сумма потоков')

    st.pyplot(fig)

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
    max_count = max(counts)
    expected_counts = poisson(lmbda * T).pmf(np.arange(0, max_count + 1)) * len(events)
    
    # Приведение массивов к одинаковой длине
    observed_counts = np.bincount(counts, minlength=len(expected_counts))
    expected_counts = expected_counts[:len(observed_counts)]
    
    # Нормализация
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

def main():
    # Пользовательский ввод
    N = st.number_input("Введите значение N", value=14)

    # Промежуток наблюдения
    T1 = N
    T2 = N + 100
    T = T2 - T1  # Время наблюдения

    # Параметры потоков
    lmbda1 = (N + 8) / (N + 24)  # Интенсивность первого потока
    lmbda2 = (N + 9) / (N + 25)  # Интенсивность второго потока

    num_realizations = 50  # Количество реализаций

    # Визуализация потоков
    events1, events2, sum_events = plot_processes(lmbda1, lmbda2, T, num_realizations)

    # Расчет статистических характеристик для каждого потока
    stats1 = compute_statistics(events1, lmbda1, T)
    stats2 = compute_statistics(events2, lmbda2, T)
    stats_sum = compute_statistics(sum_events, lmbda1 + lmbda2, T)

    # Вывод результатов
    st.subheader("Статистика для процесса с λ1={:.2f}".format(lmbda1))
    st.markdown(f"""
    - **Эмпирическая интенсивность λ**: {stats1['empirical_lambda']:.4f}
    - **Теоретическая дисперсия**: {stats1['theoretical_var']:.4f}
    - **Эмпирическая дисперсия**: {stats1['empirical_var']:.4f}
    - **Статистика Колмогорова-Смирнова**: {stats1['ks_stat']:.4f}
    - **p-значение Колмогорова-Смирнова**: {stats1['ks_pvalue']:.4f}
    - **Статистика χ²**: {stats1['chi2_stat']:.4f}
    - **p-значение χ²**: {stats1['chi2_pvalue']:.4f}
    """)

    st.subheader("Статистика для процесса с λ2={:.2f}".format(lmbda2))
    st.markdown(f"""
    - **Эмпирическая интенсивность λ**: {stats2['empirical_lambda']:.4f}
    - **Теоретическая дисперсия**: {stats2['theoretical_var']:.4f}
    - **Эмпирическая дисперсия**: {stats2['empirical_var']:.4f}
    - **Статистика Колмогорова-Смирнова**: {stats2['ks_stat']:.4f}
    - **p-значение Колмогорова-Смирнова**: {stats2['ks_pvalue']:.4f}
    - **Статистика χ²**: {stats2['chi2_stat']:.4f}
    - **p-значение χ²**: {stats2['chi2_pvalue']:.4f}
    """)

    st.subheader("Статистика для суммы процессов (λ1 + λ2)")
    st.markdown(f"""
    - **Эмпирическая интенсивность λ**: {stats_sum['empirical_lambda']:.4f}
    - **Теоретическая дисперсия**: {stats_sum['theoretical_var']:.4f}
    - **Эмпирическая дисперсия**: {stats_sum['empirical_var']:.4f}
    - **Статистика Колмогорова-Смирнова**: {stats_sum['ks_stat']:.4f}
    - **p-значение Колмогорова-Смирнова**: {stats_sum['ks_pvalue']:.4f}
    - **Статистика χ²**: {stats_sum['chi2_stat']:.4f}
    - **p-значение χ²**: {stats_sum['chi2_pvalue']:.4f}
    """)


if __name__ == "__main__":
    st.title("Моделирование пуассоновских потоков")
    main()
