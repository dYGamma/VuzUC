"""
Task 2: установившаяся ошибка e_уст при x = 100·1(t).

Аналитика:
  E(s) = X(s) / (1 + W_разомк(s))
  e_уст = lim_{s→0} s·E(s) = lim_{s→0} s·(100/s) / (1 + W_разомк(s))
        = 100 / (1 + W_разомк(0))

Разомкнутая (петлевая) ПФ W_разомк(s) = W_прямая(s)·H(s) из Task 1:
  W_open(s) = (23634000000·s + 16604400000) /
              (3·s⁴ + 9090062·s³ + 187860040·s² + 121200000·s + 0)

В знаменателе свободный множитель s → W_open(0) → ∞.
Следовательно система астатическая 1-го порядка по задающему воздействию,
и установившаяся ошибка по позиционному входу x = 100·1(t) равна нулю.

  e_уст = 100 / (1 + ∞) = 0.

Моделирование: симуляция переходного процесса по сигналу ошибки e(t).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim

# Передаточная функция замкнутой системы (Task 1):
num_cl = [1181700000.0, 24464220000.0, 16604400000.0]
den_cl = [3.0, 9090062.0, 187860040.0, 23755200000.0, 16604400000.0]

# Прямая ветвь (от e к y) — для вычисления ошибки e(t) = x(t) - y_meas(t)
# где y_meas = y / (0.05s + 1)
# Сигнал ошибки e — это вход в W1 после внешнего сумматора.
# e(s) = X(s) - y(s)·H(s), H(s) = 1/(0.05s+1)
# e(s) = X(s)·[1 - W_cl(s)·H(s)] ... не совсем. Правильно:
# e(s) = X(s)/(1 + W_open(s))
# где W_open(s) — петлевая ПФ
num_open = [23634000000.0, 16604400000.0]
den_open = [3.0, 9090062.0, 187860040.0, 121200000.0, 0.0]

# Φ_e(s) = 1/(1 + W_open(s)) = den_open / (den_open + num_open)
# Складываем полиномы:
deg = max(len(den_open), len(num_open))
def pad(p, n):
    return [0.0]*(n - len(p)) + list(p)
den_e = list(np.array(pad(den_open, deg)) + np.array(pad(num_open, deg)))
num_e = den_open  # числитель Φ_e

sys_e = lti(num_e, den_e)

# Шаг x = 100·1(t)
T = np.linspace(0, 30, 30001)
x = 100 * np.ones_like(T)
_, e_t, _ = lsim(sys_e, x, T)

# Установившееся значение
e_ss_sim = e_t[-200:].mean()
print(f"e_уст (моделирование) = {e_ss_sim:.6e}")
print(f"e_уст (аналитика)    = 0.000000 (астатизм 1-го порядка)")

# График
fig, ax = plt.subplots(figsize=(9,4.5))
ax.plot(T, e_t, lw=1.5, color='#1f77b4')
ax.axhline(0, color='k', lw=0.5, ls='--')
ax.set_xlabel('t, с')
ax.set_ylabel('e(t)')
ax.set_title('Task 2: переходный процесс сигнала ошибки e(t) при x = 100·1(t)')
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('figures/task2_error.png', dpi=130)
print("Saved figures/task2_error.png")

# Также строим y(t)
sys_y = lti(num_cl, den_cl)
_, y_t, _ = lsim(sys_y, x, T)
fig2, ax2 = plt.subplots(figsize=(9,4.5))
ax2.plot(T, y_t, lw=1.5, color='#d62728', label='y(t)')
ax2.plot(T, x, '--', color='gray', lw=1, label='x(t) = 100·1(t)')
ax2.set_xlabel('t, с')
ax2.set_ylabel('y(t)')
ax2.set_title('Task 2: переходный процесс выхода y(t) при x = 100·1(t)')
ax2.grid(True, alpha=0.4)
ax2.legend()
plt.tight_layout()
plt.savefig('figures/task2_output.png', dpi=130)
print("Saved figures/task2_output.png")
print(f"y_уст (моделирование) = {y_t[-200:].mean():.4f}")
