from sympy import symbols, Function, Derivative, dsolve, solve, sin, log, sqrt, pi

# Определяем символы
x = symbols('x')
y = Function('y')(x)
dy = Derivative(y)

# Определяем функционал
F = (y - (1/2) * dy**2) * sin(x)  # Функционал, соответствующий вашему случаю

# Находим производные
dFdy = Derivative(F, y)
dFd1y = Derivative(F, dy)

# Уравнение Эйлера-Лагранжа
L = dFdy - Derivative(dFd1y, x)
print(f'Уравнение Эйлера-Лагранжа: {L}')

# Решение уравнения
sol = dsolve(L)
print(f'Общее решение: {sol}')

# Задаем граничные условия
eq1 = sol.lhs.subs(x, pi/4) - (-log(sqrt(2)))  # y(π/4) = -ln(√2)
eq2 = sol.lhs.subs(x, pi/2)  # y(π/2) = 0

# Решаем систему уравнений для нахождения констант
coeffs = solve([eq1, eq2])
print(f'Константы: {coeffs}')

# Подставляем константы в общее решение
res = sol.subs(coeffs)
print(f'Оптимальное решение: {res}')
