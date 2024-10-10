from sympy import symbols, Function, Derivative, dsolve, solve, sin, log, pi, Eq, tan, lambdify
import numpy as np
import matplotlib.pyplot as plt

# Определяем символы
x = symbols('x')
C1, C2 = symbols('C1 C2')  # Константы
y = Function('y')(x)
dy = Derivative(y, x)

# Определяем функционал
F = (y - (1/2) * dy**2) * sin(x)  # Функционал

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
eq1 = Eq(sol.rhs.subs(x, pi/4), -log(2)/2)  # y(π/4) = -ln(√2)
eq2 = Eq(sol.rhs.subs(x, pi/2), 0)          # y(π/2) = 0

# Решаем систему уравнений для нахождения констант
coeffs = solve([eq1, eq2], [C1, C2])
print(f'Константы: {coeffs}')

# Подставляем константы в общее решение
res = sol.subs(coeffs)
print(f'Оптимальное решение: {res}')

# Проверка решения на граничные условия
check_eq1 = eq1.subs(coeffs)
check_eq2 = eq2.subs(coeffs)
print(f'Проверка y(π/4): {check_eq1}, y(π/2): {check_eq2}')

# Проверка, если res является уравнением
if isinstance(res, Eq):
    # Создаем числовую функцию для графика, используя NumPy для логарифма
    y_func = lambdify(x, res.rhs, 'numpy')
    
    # Графический вывод
    x_vals = np.linspace(0, np.pi, 100)  # Используем np.pi вместо sympy.pi
    y_vals = y_func(x_vals)  # Получаем численные значения y

    # Избегаем проблем с логарифмами
    y_vals = np.where(np.tan(x_vals / 2) > 0, y_vals, np.nan)  # Заменяем недопустимые значения на NaN

    # Строим график
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label='Оптимальное решение')
    plt.title('График оптимального решения')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(np.pi/4, color='red', lw=0.5, ls='--', label='x = π/4')
    plt.axvline(np.pi/2, color='green', lw=0.5, ls='--', label='x = π/2')
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Решение не является уравнением или не найдено.")
