import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, log, tan

# Определяем переменные
x = symbols('x')

# Определяем функцию для y(x)
def y_function(x_vals):
    return -np.log(np.tan(x_vals / 2)**2 + 1) + np.log(np.tan(x_vals / 2)) + 0.693147180559945

# Генерируем значения x от π/4 до π/2
x_vals = np.linspace(np.pi/4, np.pi/2, 500)
y_vals = y_function(x_vals)

# Построение графика
plt.plot(x_vals, y_vals, label=r'$y(x) = -\log(\tan^2(x/2) + 1) + \log(\tan(x/2)) + 0.693$')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('График оптимального решения вариационной задачи')
plt.grid(True)
plt.legend()
plt.show()
