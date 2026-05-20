"""
Task 5: нелинейный логический регулятор (формула из ТЗ).
Реализация через явную схему Эйлера с малым шагом.
"""

import numpy as np
import matplotlib.pyplot as plt

DELTA = 1.0
K_GAIN = 1.0

# Объект — редуцированная W из Task 1
A_W = np.array([[0,1],[-2599.6, -19.96]])
B_W = np.array([0.0, 1.0])
C_W = np.array([2600.0, 130.0])

dt = 1e-4
T_end = 30
N = int(T_end/dt) + 1
t_arr = np.linspace(0, T_end, N)

# Состояния:
x_W = np.zeros(2)
# Lead-фильтры (2s+1)/(Ts+1) реализуем как:
#   x_dot = (-1/T)·x + (1 - 2/T)/T · u
#   y     = 2/T · u + x
# Так выход содержит мгновенную проекцию ⇒ хранится только одно состояние
T5 = 5.0; T3 = 3.0
x_lead5 = 0.0
x_lead3 = 0.0
# 18/(0.05s+1)
T18 = 0.05; K18 = 18.0
x_18 = 0.0

x_ref = 100.0
y_log = np.zeros(N)
F_log = np.zeros(N)

for i in range(N):
    y = C_W @ x_W
    e = x_ref - y

    # Lead-фильтры
    lead5_out = 2.0/T5 * e + x_lead5
    lead3_out = 2.0/T3 * e + x_lead3

    # 18/(0.05s+1) применяется к lead5_out
    h18_out = x_18  # выход = состояние

    # Логика регулятора
    if e > 10:
        g1 = lead5_out
    else:
        g1 = lead3_out

    if abs(g1) > 7:
        z_signal = h18_out
    else:
        z_signal = 5.0 * lead3_out

    if abs(z_signal) <= DELTA:
        F_val = 0.0
    else:
        F_val = K_GAIN * z_signal - DELTA * np.sign(z_signal)

    y_log[i] = y
    F_log[i] = F_val

    # Обновление состояний (Forward Euler)
    dx_lead5 = -1/T5 * x_lead5 + (1 - 2/T5)/T5 * e
    dx_lead3 = -1/T3 * x_lead3 + (1 - 2/T3)/T3 * e
    dx_18    = -1/T18 * x_18 + K18/T18 * lead5_out
    dx_W = A_W @ x_W + B_W * F_val

    x_lead5 += dt * dx_lead5
    x_lead3 += dt * dx_lead3
    x_18    += dt * dx_18
    x_W     += dt * dx_W

y_ss = y_log[-1000:].mean()
sigma = (y_log.max() - y_ss)/y_ss*100 if y_ss>0 else 0
tube = 0.05*abs(y_ss)
idx_out = np.where(np.abs(y_log - y_ss) > tube)[0]
t_pp = t_arr[idx_out[-1]] if len(idx_out) else 0
print(f"y_уст = {y_ss:.3f}")
print(f"σ     = {sigma:.2f} %")
print(f"t_пп (5%) = {t_pp:.3f} с")

fig, axes = plt.subplots(2,1, figsize=(10,7), sharex=True)
axes[0].plot(t_arr, y_log, lw=1.4, color='#1f77b4', label='y(t)')
axes[0].axhline(x_ref, color='gray', ls='--', lw=1, label=f'x={x_ref}')
axes[0].axhline(y_ss*1.05, color='orange', ls=':', lw=0.7, label='5% трубка')
axes[0].axhline(y_ss*0.95, color='orange', ls=':', lw=0.7)
axes[0].set_ylabel('y(t)')
axes[0].set_title(f'Task 5: переходный процесс. y_уст={y_ss:.2f}, σ={sigma:.1f}%, t_пп={t_pp:.2f}с')
axes[0].grid(True, alpha=0.4); axes[0].legend(loc='lower right')

axes[1].plot(t_arr, F_log, lw=1.2, color='#d62728', label='F(e)')
axes[1].set_xlabel('t, с'); axes[1].set_ylabel('F(e)')
axes[1].grid(True, alpha=0.4); axes[1].legend(loc='upper right')
plt.tight_layout()
plt.savefig('figures/task5_nlreg.png', dpi=130)
print("Saved figures/task5_nlreg.png")
