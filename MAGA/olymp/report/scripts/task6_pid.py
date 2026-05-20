"""
Task 6: ПИД-регулятор с экстраполятором нулевого порядка (ZOH) в обратной связи
и временной задержкой τ = 1.5 с в прямой ветви.

Требования:
  σ ≤ 30 %, t_пп ≤ 10 с, y_уст = 20 при x = 100·1(t).

Структура: x → [+/-] → e → ПИД → delay(τ=1.5) → W → y
                          ▲                              │
                          └── ZOH(T_zoh) ───────────────┘

Объект W — редуцированная модель из Task 1.
Для y_уст=20 при x=100 нужен статический коэф. замкнутой системы 0.2 ⇒
предкомпенсатор/масштабирование уставки = 0.2. Регулятор работает по ошибке
e = 0.2·x − y_meas. С ПИД (интегратор → астатизм) y_меас выходит на 0.2·x = 20.
"""

import numpy as np
import matplotlib.pyplot as plt

# Редуцированная модель объекта
A_W = np.array([[0,1],[-2599.6, -19.96]])
B_W = np.array([0.0, 1.0])
C_W = np.array([2600.0, 130.0])

# Параметры
TAU_DELAY = 1.5
T_ZOH = 0.1
SETPOINT_SCALE = 0.2  # масштабирование уставки: 100·0.2 = 20
x_amp = 100.0
T_end = 40
dt = 1e-3

def simulate(Kp, Ki, Kd):
    N = int(T_end/dt)+1
    t_arr = np.linspace(0, T_end, N)

    x_W = np.zeros(2)
    int_e = 0.0
    prev_e = 0.0

    # Буфер задержки
    n_delay = int(TAU_DELAY/dt)
    u_buffer = np.zeros(n_delay)

    # ZOH в ОС
    y_zoh = 0.0
    zoh_counter = 0
    n_zoh = max(1, int(T_ZOH/dt))

    y_log = np.zeros(N)
    for i in range(N):
        y_now = (C_W @ x_W).item()
        y_log[i] = y_now

        # ZOH update
        if i % n_zoh == 0:
            y_zoh = y_now

        # Ошибка с масштабированной уставкой
        e = SETPOINT_SCALE * x_amp - y_zoh

        # ПИД
        int_e += e * dt
        der_e = (e - prev_e) / dt
        u = Kp*e + Ki*int_e + Kd*der_e
        prev_e = e

        # Задержка
        u_delayed = u_buffer[0]
        u_buffer = np.roll(u_buffer, -1)
        u_buffer[-1] = u

        # Динамика объекта
        dx = A_W @ x_W + B_W * u_delayed
        x_W = x_W + dt * dx

    return t_arr, y_log

def stepinfo(t, y, y_set=20):
    y_ss = y[-200:].mean()
    sigma = (y.max() - y_ss)/y_ss*100 if y_ss>0 else 0
    tube = 0.05*abs(y_set)
    idx = np.where(np.abs(y - y_set) > tube)[0]
    t_pp = t[idx[-1]] if len(idx) else 0
    return y_ss, sigma, t_pp

# Подбор параметров ПИД
print("Подбор параметров ПИД...")
best = None
candidates = []
for Kp in [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]:
    for Ki in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35]:
        candidates.append((Kp, Ki, 0.0))
for (Kp, Ki, Kd) in candidates:
    t_a, y_a = simulate(Kp, Ki, Kd)
    y_ss, sg, tp = stepinfo(t_a, y_a, 20)
    # фильтруем явно неустойчивые
    if y_ss > 50 or y_ss < 10 or sg > 200:
        continue
    score = (max(0, sg-30)*2 + max(0, tp-10) + abs(y_ss-20)*5)
    if best is None or score < best[0]:
        best = (score, Kp, Ki, Kd, y_ss, sg, tp, t_a, y_a)
        print(f"  *NEW BEST* Kp={Kp}, Ki={Ki}: y_уст={y_ss:.2f}, σ={sg:.2f}%, t_пп={tp:.2f}с, score={score:.2f}")

_, Kp, Ki, Kd, y_ss, sg, tp, t_a, y_a = best
print(f"\nЛУЧШИЙ: Kp={Kp}, Ki={Ki}, Kd={Kd}")
print(f"  y_уст = {y_ss:.2f}")
print(f"  σ     = {sg:.2f} %")
print(f"  t_пп  = {tp:.2f} с")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(t_a, y_a, lw=1.5, color='#1f77b4', label=f'y(t), Kp={Kp}, Ki={Ki}, Kd={Kd}')
ax.axhline(20, color='gray', ls='--', lw=1, label='y_уст = 20')
ax.axhline(20*1.05, color='orange', ls=':', lw=0.7, label='5% трубка')
ax.axhline(20*0.95, color='orange', ls=':', lw=0.7)
ax.axhline(20*1.30, color='red', ls=':', lw=0.7, label='σ=30%')
ax.set_xlabel('t, с'); ax.set_ylabel('y(t)')
ax.set_title(f'Task 6: ПИД с задержкой τ=1.5с и ZOH в ОС. σ={sg:.1f}%, t_пп={tp:.2f}с')
ax.grid(True, alpha=0.4); ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figures/task6_pid.png', dpi=130)
print("Saved figures/task6_pid.png")
