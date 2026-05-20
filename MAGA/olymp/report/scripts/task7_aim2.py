"""
Task 7: реализация АИМ-2 (амплитудно-импульсного модулятора 2-рода).

Период прерывания T = 1 с, ширина импульса γ = 60 % (γT = 0.6 с).
АИМ-2 «вырезает» входной сигнал на интервалах [nT, nT+γT),
вне импульса выход = 0.

Реализация в Simulink через MATLAB Function блок:
  function y = aim2(u, t)
      T = 1.0;
      gamma = 0.6;
      phase = mod(t, T);
      if phase < gamma*T
          y = u;
      else
          y = 0;
      end
  end

Для визуализации — синусоидальный вход.
"""

import numpy as np
import matplotlib.pyplot as plt

T_period = 1.0
gamma = 0.6
freq = 0.3  # Hz входного синуса

t = np.linspace(0, 10, 10001)
x = np.sin(2*np.pi*freq*t)

phase = np.mod(t, T_period)
mask = phase < gamma*T_period
y = np.where(mask, x, 0.0)

fig, ax = plt.subplots(figsize=(11,4.5))
ax.plot(t, x, '--', color='gray', lw=1, label='x(t) = sin(2π·0.3·t)')
ax.plot(t, y, color='#1f77b4', lw=1.4, label='x*(t) — выход АИМ-2')
# заштрихуем интервалы импульса
for k in range(int(t[-1]/T_period)+1):
    ax.axvspan(k*T_period, k*T_period + gamma*T_period, color='orange', alpha=0.1)
ax.set_xlabel('t, с'); ax.set_ylabel('сигнал')
ax.set_title(f'Task 7: АИМ-2, T={T_period}с, γ={gamma*100:.0f}%')
ax.grid(True, alpha=0.4); ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('figures/task7_aim2.png', dpi=130)
print("Saved figures/task7_aim2.png")
