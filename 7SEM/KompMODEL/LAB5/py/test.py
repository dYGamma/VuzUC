import numpy as np
from scipy.integrate import solve_ivp

alpha_val = 5
beta_val = 8
gamma_val = 1.9
mu_val = 2.1
lambda_val = 3.16
delta_val = 0.9
rho_val = 0.5
T1_val = 0.3
time_interval = 20
time_points = np.linspace(0, time_interval, 1000)
initial_conditions = [1, 1, 1]

# Функции для вашей системы и целевой функции
def system(t, vars, rho, T1):
    Y1, Y2, Y3 = vars
    psi1 = Y3 - rho * Y2
    u1 = lambda_val * Y3 - delta_val * Y2 + rho * (mu_val * (Y2 + Y3) - beta_val * Y1 * Y3) - psi1 / T1
    dY1_dt = alpha_val * Y2 * Y3 - gamma_val * Y1
    dY2_dt = mu_val * (Y2 + Y3) - beta_val * Y1 * Y3
    dY3_dt = delta_val * Y2 - lambda_val * Y3 + u1
    return [dY1_dt, dY2_dt, dY3_dt]


def cost_function(rho, T1, time_interval=20, time_points=np.linspace(0, 20, 1000), initial_conditions=[1, 1, 1]):
    sol = solve_ivp(system, [0, time_interval], initial_conditions, t_eval=time_points, args=(rho, T1))
    Y1, Y2, Y3 = sol.y

    # Например, ошибка может быть разницей между Y1 и его желаемым значением (например, 0)
    error = np.sum(np.abs(Y1 - 0.5))  # Ошибка на всех точках времени

    return error


# Градиентный спуск
def gradient_descent(initial_rho, initial_T1, learning_rate=0.01, max_iterations=100, epsilon=0.5):
    rho = initial_rho
    T1 = initial_T1
    for _ in range(max_iterations):
        # Вычисляем ошибку для текущих параметров
        error_current = cost_function(rho, T1)

        # Приближение градиента (используем малое изменение для численного градиента)
        delta_rho = 1e-4
        delta_T1 = 1e-4
        error_rho = cost_function(rho + delta_rho, T1) - error_current
        error_T1 = cost_function(rho, T1 + delta_T1) - error_current

        # Обновление параметров
        rho_new = rho - learning_rate * error_rho / delta_rho
        T1_new = T1 - learning_rate * error_T1 / delta_T1

        # Проверка сходимости
        if np.abs(cost_function(rho_new, T1_new) - error_current) < epsilon:
            break

        # Обновляем параметры
        rho, T1 = rho_new, T1_new

    return rho, T1


# Начальные значения
initial_rho = 1.0
initial_T1 = 0.1

# Оптимизация
optimal_rho, optimal_T1 = gradient_descent(initial_rho, initial_T1)
print(f"Optimal rho: {optimal_rho}, Optimal T1: {optimal_T1}")
