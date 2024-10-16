import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Function, Derivative, dsolve, Eq, sin, log, pi, solve

# Определяем символы
x = symbols('x')
y = Function('y')(x)
dy = Derivative(y, x)

# Определяем константы C1 и C2
C1, C2 = symbols('C1 C2')

# Определяем лагранжиан (L)
L = (y - (1/2) * dy**2) * sin(x)

# Вычисляем частные производные
dL_dy = L.diff(y)  # Частная производная L по y
dL_ddy = L.diff(dy)  # Частная производная L по dy
d_dx_dL_ddy = Derivative(dL_ddy, x).doit()  # Производная по x от dL_ddy

# Уравнение Эйлера-Лагранжа
euler_lagrange_eq = Eq(d_dx_dL_ddy - dL_dy, 0)
print(f'Уравнение Эйлера-Лагранжа: {euler_lagrange_eq}')

# Решаем уравнение Эйлера-Лагранжа
sol = dsolve(euler_lagrange_eq)
print(f'Общее решение: {sol}')

# Задаем граничные условия: y(π/4) = -ln(√2) и y(π/2) = 0
boundary_conditions = [
    Eq(sol.rhs.subs(x, pi/4), -log(np.sqrt(2))),  # y(π/4) = -ln(√2)
    Eq(sol.rhs.subs(x, pi/2), 0)                  # y(π/2) = 0
]

# Решаем для нахождения констант
constants = solve(boundary_conditions, (C1, C2))  # Обязательно указываем константы
print(f'Найденные константы: {constants}')

# Подставляем константы в общее решение
final_solution = sol.subs(constants)
print(f'Оптимальное решение: {final_solution}')

# Переходим к построению графика решения y(x) = ln|sin(x)|
def y_func(x_vals):
    return np.log(np.abs(np.sin(x_vals)))

# Генерируем значения x от π/4 до π/2
x_vals = np.linspace(np.pi/4, np.pi/2, 500)
y_vals = y_func(x_vals)

# Построение графика
plt.plot(x_vals, y_vals, label=r'$y(x) = \ln|\sin(x)|$')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('График решения вариационной задачи')
plt.grid(True)
plt.legend()
plt.show()
