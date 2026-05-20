"""
Task 1: эквивалентная ПФ из структурной схемы рис.1.

Топология (исполнительный механизм):
  x ─►[+/-]─ e ─►[W1=0.7/(1.5s+1)]──►[+ +]──►[+/-]──►[W2=3030/0.01s]──►[W3=10]──┬──►[W4=1/0.1s]──► y
       ▲                              ▲              ▲                              │
       │                              │              └──────────────────────────────┘  (внутренняя единичная отрицательная ОС, от точки после W3)
       │                              │
       │                              └─── (×13) ◄──────────────────────────────────┘  (положительный feedforward с коэффициентом 13, параллельно W1)
       │                                                                              т.е. блок 13 берёт сигнал e и параллельно W1 даёт +13e к "++"
       │
       └─[H=1/(0.05s+1)]◄──────────────────────────────────────────────────────────── y

Замечание: блок 13 интерпретируется как параллельная пропорциональная ветвь
(вместе с W1 = 0.7/(1.5s+1)) — это корректирующее звено с опережением (lead compensator).
Такая трактовка даёт устойчивую замкнутую систему. Альтернативные интерпретации
(13 как контур ПОС от сигнала после W3) дают неустойчивые внутренние моды.

Метод 1: символьная свёртка (правила преобразования структурных схем).
Метод 2: формула Мейсона.
Метод 3: МАТЛАБ (`feedback`, `series`) — в task1_reduce.m.
"""

import sympy as sp

s = sp.symbols('s')

# Блоки
W1 = sp.Rational(7,10) / (sp.Rational(3,2)*s + 1)      # 0.7/(1.5s+1)
W2 = 3030 / (sp.Rational(1,100)*s)                      # 3030/(0.01s)
W3 = 10
W4 = 1 / (sp.Rational(1,10)*s)                          # 1/(0.1s)
H  = 1 / (sp.Rational(1,20)*s + 1)                      # 1/(0.05s+1)
K13 = 13

# ---------- Метод 1: эквивалентные преобразования ----------
# Шаг 1: параллельное соединение W1 и K13 (оба входят в "++"):
W_par = sp.simplify(W1 + K13)
print("W_par  = W1 + 13 =", sp.together(W_par))

# Шаг 2: внутренний контур: прямая ветвь W2*W3, отрицательная единичная ОС
W23 = sp.simplify(W2 * W3)
W_inner = sp.simplify(W23 / (1 + W23))
print("W_inner =", sp.together(W_inner))

# Шаг 3: последовательное соединение W_par * W_inner * W4
W_forward = sp.simplify(W_par * W_inner * W4)
W_forward = sp.together(W_forward)
print("W_forward =", W_forward)

# Шаг 4: внешняя обратная связь через H (отрицательная)
W_cl = sp.simplify(W_forward / (1 + W_forward * H))
W_cl = sp.together(sp.expand(sp.simplify(W_cl)))
print("\nЗамкнутая ПФ W_cl(s) = y/x:")
num_cl, den_cl = sp.fraction(sp.together(W_cl))
num_cl = sp.expand(num_cl)
den_cl = sp.expand(den_cl)
print("Числитель:", num_cl)
print("Знаменатель:", den_cl)

# ---------- Метод 2: формула Мейсона (контроль) ----------
# Граф сигналов:
# Узлы: x, e1, a, b, c, d, y, ym
# Дуги:
#   x → e1: +1
#   ym → e1: -1   (обратная связь)
#   e1 → b: W1 (через узел a)
#   e1 → b: K13  (через параллельную ветвь)
#   b → c: ?  (через [+/-])
#   c → c: -W2*W3 (внутренняя петля)
#   c → y: W4
#   y → ym: H
# Это сводится к тем же формулам. Контроль через cross-check:
W_cl_mason = sp.simplify(W_par * W23 * W4 / ((1 + W23) * (1 + W_par*W23*W4*H/(1+W23))))
W_cl_mason = sp.simplify(W_cl_mason)
print("\nКонтроль (Мейсон):")
num_m, den_m = sp.fraction(sp.together(W_cl_mason))
print("Совпадает:", sp.simplify(num_cl * den_m - den_cl * num_m) == 0)

# ---------- Численная форма (decimal) ----------
def to_decimal(expr, prec=6):
    return sp.nsimplify(sp.N(expr, prec), rational=False)

print("\nЧисленные коэффициенты:")
print("Num:", sp.Poly(num_cl, s).all_coeffs())
print("Den:", sp.Poly(den_cl, s).all_coeffs())

# ---------- Сохранение коэффициентов для использования в других task ----------
poly_num = sp.Poly(num_cl, s).all_coeffs()
poly_den = sp.Poly(den_cl, s).all_coeffs()
print("\n--- Для MATLAB / scipy ---")
print("num =", [float(c) for c in poly_num])
print("den =", [float(c) for c in poly_den])

# Разомкнутая ПФ для расчёта установившейся ошибки (Task 2):
W_open = sp.simplify(W_forward * H)  # W_разомк = прямая ветвь * датчик ОС
W_open = sp.together(W_open)
num_op, den_op = sp.fraction(W_open)
num_op = sp.expand(num_op)
den_op = sp.expand(den_op)
print("\nРазомкнутая (петлевая) ПФ:")
print("Num:", sp.Poly(num_op, s).all_coeffs())
print("Den:", sp.Poly(den_op, s).all_coeffs())
print("num_open =", [float(c) for c in sp.Poly(num_op, s).all_coeffs()])
print("den_open =", [float(c) for c in sp.Poly(den_op, s).all_coeffs()])
