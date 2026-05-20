"""
Task 4: аппроксимация нелинейной характеристики F(e) и оценка влияния
на переходный процесс замкнутой системы (рис.2).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

e_data = np.array([-50, -45, -30, -20, 0, 20, 30, 45, 50], dtype=float)
F_data = np.array([2.85, 2, 1.7, 1.4, 0, 1.4, 1.7, 2, 2.85])

# ---------- Аппроксимации ----------
def F_pwl(e):
    e_arr = np.atleast_1d(e)
    res = np.interp(e_arr, e_data, F_data)
    # симметрично продлеваем за пределы
    return res if e_arr.ndim else res.item()

abs_e = np.abs(e_data)
poly_coef = np.polyfit(abs_e, F_data, 3)
def F_poly(e):
    return np.polyval(poly_coef, np.abs(e))

mask = abs_e > 0
b, log_a = np.polyfit(np.log(abs_e[mask]), np.log(F_data[mask]), 1)
a_pow = np.exp(log_a)
def F_pow(e):
    return a_pow * np.power(np.maximum(np.abs(e), 1e-12), b)

print(f"Полином 3-й ст.:    F(e) = {poly_coef[0]:+.4e}|e|³ {poly_coef[1]:+.4e}|e|² {poly_coef[2]:+.4e}|e| {poly_coef[3]:+.4f}")
print(f"Степенная:          F(e) = {a_pow:.4f}·|e|^{b:.4f}")

# ---------- Визуализация ----------
e_grid = np.linspace(-60, 60, 1201)
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(e_data, F_data, 'ko', ms=8, label='Точки таблицы')
ax.plot(e_grid, F_pwl(e_grid),  '-',  lw=1.5, label='Кусочно-линейная')
ax.plot(e_grid, F_poly(e_grid), '--', lw=1.5, label='Полином 3-й ст.')
ax.plot(e_grid, F_pow(e_grid),  ':',  lw=2,   label=f'Степенная: {a_pow:.3f}·|e|^{b:.3f}')
ax.set_xlabel('e'); ax.set_ylabel('F(e)')
ax.set_title('Task 4: аппроксимации F(e)')
ax.grid(True, alpha=0.4); ax.legend()
plt.tight_layout()
plt.savefig('figures/task4_approx.png', dpi=130)

# ---------- Редуцированная модель объекта (после сокращения быстрого полюса) ----------
# W_red(s) ≈ 130·(s+20) / (s² + 19.96s + 2599.6)
# (быстрый полюс s≈-3·10⁶ исключён; полюс/нуль ≈-0.7 сокращены)
num_W = np.array([130.0, 130.0*20])
den_W = np.array([1.0, 19.96, 2599.6])

# State-space (controllable canonical):
# ẋ₁ = x₂
# ẋ₂ = -2599.6·x₁ - 19.96·x₂ + u
# y   = 130·20·x₁ + 130·x₂ = 2600·x₁ + 130·x₂
A = np.array([[0,1],[-2599.6, -19.96]])
B = np.array([0,1])
C = np.array([2600.0, 130.0])

def simulate(F_func, T_end=10, x_amp=100):
    def rhs(t, state):
        y = C @ state
        e_sig = x_amp - y
        u = F_func(np.array([e_sig]))[0] if hasattr(F_func(np.array([0.0])), '__iter__') else float(F_func(e_sig))
        return A @ state + B*u
    sol = solve_ivp(rhs, [0, T_end], [0,0], max_step=0.005, dense_output=True, rtol=1e-8, atol=1e-10)
    t_arr = np.linspace(0, T_end, 5001)
    states = sol.sol(t_arr)
    y_arr = C @ states
    return t_arr, y_arr

T_end = 8
fig2, ax2 = plt.subplots(figsize=(10,5))
colors = ['#1f77b4','#d62728','#2ca02c']
table = []
for (name, Ff), c in zip([('Кусочно-линейная', F_pwl),('Полином 3-й ст.', F_poly),('Степенная', F_pow)], colors):
    t_a, y_a = simulate(Ff, T_end=T_end)
    y_ss = y_a[-200:].mean()
    sg = (y_a.max() - y_ss)/y_ss*100 if y_ss>0 else 0
    tube = 0.05*abs(y_ss)
    idx = np.where(np.abs(y_a - y_ss) > tube)[0]
    tp = t_a[idx[-1]] if len(idx) else 0
    table.append((name, y_ss, sg, tp))
    ax2.plot(t_a, y_a, color=c, lw=1.5,
             label=f'{name}: y_уст={y_ss:.1f}, σ={sg:.1f}%, t_пп={tp:.2f}с')
    print(f"{name}: y_уст={y_ss:.2f}, σ={sg:.2f}%, t_пп={tp:.3f}с")

ax2.axhline(100, color='gray', ls='--', lw=1, label='x=100')
ax2.set_xlabel('t, с'); ax2.set_ylabel('y(t)')
ax2.set_title('Task 4: переходные процессы для разных аппроксимаций F(e)')
ax2.grid(True, alpha=0.4); ax2.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figures/task4_compare.png', dpi=130)
print("Saved figures/task4_compare.png")

# Сохраняем таблицу
with open('figures/task4_table.txt','w',encoding='utf-8') as f:
    f.write("Аппроксимация | y_уст | σ, % | t_пп, с\n")
    for n, ys, sg, tp in table:
        f.write(f"{n} | {ys:.2f} | {sg:.2f} | {tp:.2f}\n")
