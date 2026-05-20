"""
Task 3: синтез линейного регулятора (рис.2).

Требования:
  - y_уст = 80 при x = 100·1(t)
  - σ ≤ 30 %
  - t_пп ≤ 7 с

Объект W — ПФ замкнутой системы из Task 1 (исполнительный механизм рис.1).
W(0) = 1 (астатизм по позиции).

Метод 1 (П-регулятор по статике): Reg = K_p.
   y_уст/x = K_p·W(0)/(1+K_p·W(0)) = 0.8 ⟹ K_p = 4.
Метод 2 (ПД-регулятор): Reg = K_p·(1 + T_d·s).
   Добавление D-составляющей для уменьшения σ.
Метод 3 (предкомпенсатор + П): масштабирование уставки 0.8 + петля с большим K_p
   для уменьшения t_пп.

В отчёте обсуждены все три. Здесь вычисляем σ, t_пп для каждого.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim, TransferFunction
from numpy.polynomial import polynomial as P

# Объект (W из Task 1)
num_W = [1181700000.0, 24464220000.0, 16604400000.0]
den_W = [3.0, 9090062.0, 187860040.0, 23755200000.0, 16604400000.0]

def series(numA, denA, numB, denB):
    return list(np.polymul(numA, numB)), list(np.polymul(denA, denB))

def feedback_unity(num_ol, den_ol):
    # Closed-loop = num_ol / (den_ol + num_ol)
    L = max(len(num_ol), len(den_ol))
    pad = lambda p: [0]*(L-len(p)) + list(p)
    den_cl = list(np.array(pad(den_ol)) + np.array(pad(num_ol)))
    return list(num_ol), den_cl

def stepinfo(t, y, y_ss):
    sigma = (y.max() - y_ss) / y_ss * 100 if y_ss > 0 else 0
    # t_пп: 5% tube
    tube = 0.05 * abs(y_ss)
    idx_out = np.where(np.abs(y - y_ss) > tube)[0]
    t_pp = t[idx_out[-1]] if len(idx_out) else t[0]
    return sigma, t_pp

T = np.linspace(0, 15, 15001)
x = 100 * np.ones_like(T)

results = {}

# ---------- Метод 1: П-регулятор K_p = 4 ----------
Kp = 4.0
num_reg, den_reg = [Kp], [1.0]
num_ol, den_ol = series(num_reg, den_reg, num_W, den_W)
num_cl, den_cl = feedback_unity(num_ol, den_ol)
sys1 = lti(num_cl, den_cl)
_, y1, _ = lsim(sys1, x, T)
y_ss1 = y1[-200:].mean()
sig1, tpp1 = stepinfo(T, y1, y_ss1)
results['P (K_p=4)'] = (y1, y_ss1, sig1, tpp1)
print(f"М1 П-регулятор K_p={Kp}: y_уст={y_ss1:.2f}, σ={sig1:.2f}%, t_пп={tpp1:.2f}с")

# ---------- Метод 2: ПД-регулятор ----------
# Reg = K_p·(1 + T_d·s); для статики K_p = 4 неизменно. Подбираем T_d.
Kp2 = 4.0
for Td in [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]:
    num_reg = [Kp2*Td, Kp2]
    den_reg = [1.0]
    num_ol, den_ol = series(num_reg, den_reg, num_W, den_W)
    num_cl, den_cl = feedback_unity(num_ol, den_ol)
    sys2 = lti(num_cl, den_cl)
    _, y2, _ = lsim(sys2, x, T)
    y_ss2 = y2[-200:].mean()
    sig2, tpp2 = stepinfo(T, y2, y_ss2)
    print(f"  ПД Td={Td}: y_уст={y_ss2:.2f}, σ={sig2:.2f}%, t_пп={tpp2:.2f}с")

# Лучший вариант:
Td_best = 0.1
num_reg = [Kp2*Td_best, Kp2]
den_reg = [1.0]
num_ol, den_ol = series(num_reg, den_reg, num_W, den_W)
num_cl, den_cl = feedback_unity(num_ol, den_ol)
sys2 = lti(num_cl, den_cl)
_, y2, _ = lsim(sys2, x, T)
y_ss2 = y2[-200:].mean()
sig2, tpp2 = stepinfo(T, y2, y_ss2)
results[f'PD (K_p=4, T_d={Td_best})'] = (y2, y_ss2, sig2, tpp2)
print(f"М2 ПД-регулятор K_p={Kp2}, T_d={Td_best}: σ={sig2:.2f}%, t_пп={tpp2:.2f}с")

# ---------- Метод 3: предкомпенсатор + большой K_p ----------
# Масштабируем уставку: x_eff = 0.8·x ⟹ при x=100 уставка для регулятора = 80
# Тогда регулятор может быть с большим K_p (петля с unity feedback на сигнал y)
# ⟹ замкнутая система: y_уст ≈ 0.8·x (т.к. большой коэф.) и быстрая.
# Эквивалентно: Reg = K_p, входной множитель 0.8, обратная связь от y.
# y/x = 0.8·K_p·W/(1+K_p·W). Для y_уст=80 при x=100: 0.8·K_p/(1+K_p) ≈ 0.8 ⟹ K_p→∞.
# Берём K_p = 20.
Kp3 = 20.0
prescale = 0.8 * (1 + Kp3) / Kp3   # чтобы получить ровно 80 в установе
# y_уст/x = prescale·K_p/(1+K_p) = 0.8 ⟹ prescale = 0.8·(1+K_p)/K_p
num_reg = [Kp3]; den_reg = [1.0]
num_ol, den_ol = series(num_reg, den_reg, num_W, den_W)
num_cl, den_cl = feedback_unity(num_ol, den_ol)
# Преобразование с входным масштабом: y = prescale·W_cl·x
num_cl = list(np.array(num_cl) * prescale)
sys3 = lti(num_cl, den_cl)
_, y3, _ = lsim(sys3, x, T)
y_ss3 = y3[-200:].mean()
sig3, tpp3 = stepinfo(T, y3, y_ss3)
results[f'P (K_p={Kp3}) + предкомп. {prescale:.4f}'] = (y3, y_ss3, sig3, tpp3)
print(f"М3 K_p={Kp3} + предкомп: y_уст={y_ss3:.2f}, σ={sig3:.2f}%, t_пп={tpp3:.2f}с")

# ---------- График ----------
fig, ax = plt.subplots(figsize=(10,5))
colors = ['#1f77b4', '#d62728', '#2ca02c']
for (name, (y, y_ss, sig, tpp)), c in zip(results.items(), colors):
    ax.plot(T, y, lw=1.5, color=c,
            label=f'{name}: σ={sig:.1f}%, t_пп={tpp:.2f}с')
ax.axhline(80, color='gray', ls='--', lw=1, label='y_уст=80')
ax.axhline(80*1.05, color='gray', ls=':', lw=0.7)
ax.axhline(80*0.95, color='gray', ls=':', lw=0.7)
ax.set_xlabel('t, с'); ax.set_ylabel('y(t)')
ax.set_title('Task 3: переходные процессы для трёх методов синтеза')
ax.grid(True, alpha=0.4); ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figures/task3_compare.png', dpi=130)
print("Saved figures/task3_compare.png")
