import streamlit as st
import pulp

# Функция для решения задачи оптимизации
def solve_optimization_problem(labor, metal, plastic, paint):
    # Создаем задачу для максимизации прибыли
    model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

    # Определяем переменные (целочисленные переменные x1, x2, x3, x4, x5)
    x1 = pulp.LpVariable('x1', lowBound=0, cat='Integer')
    x2 = pulp.LpVariable('x2', lowBound=0, cat='Integer')
    x3 = pulp.LpVariable('x3', lowBound=0, cat='Integer')
    x4 = pulp.LpVariable('x4', lowBound=0, cat='Integer')
    x5 = pulp.LpVariable('x5', lowBound=0, cat='Integer')

    # Целевая функция: максимизация прибыли
    model += 40 * x1 + 70 * x2 + 120 * x3 + 120 * x4 + 50 * x5, "Profit"

    # Ограничения по ресурсам
    model += 2 * x1 + 3 * x2 + 5 * x3 + 4 * x4 + 4 * x5 <= labor  # Трудозатраты
    model += 2 * x1 + 2 * x2 + 4 * x3 + 5 * x4 + 0 * x5 <= metal  # Металл
    model += 1 * x1 + 3 * x2 + 2 * x3 + 0 * x4 + 4 * x5 <= plastic  # Пластик
    model += 1 * x1 + 2 * x2 + 3 * x3 + 3 * x4 + 2 * x5 <= paint  # Краска

    # Решение задачи
    model.solve()

    # Возвращаем результаты
    return {
        "x1": x1.varValue,
        "x2": x2.varValue,
        "x3": x3.varValue,
        "x4": x4.varValue,
        "x5": x5.varValue,
        "profit": pulp.value(model.objective)
    }

# Streamlit интерфейс
st.title("Оптимизация производства холодильников")

# Создаем две колонки: одну для ввода данных, другую для отображения результатов
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Введите доступные ресурсы:")
    
    # Поля для ввода ресурсов
    labor = st.number_input("Трудозатраты (чел.-ч):", min_value=0, value=900, step=1)
    metal = st.number_input("Металл (м²):", min_value=0, value=8500, step=1)
    plastic = st.number_input("Пластик (м²):", min_value=0, value=4000, step=1)
    paint = st.number_input("Краска (кг):", min_value=0, value=5000, step=1)

with col2:
    if st.button("Рассчитать оптимальное количество"):
        # Решаем задачу оптимизации
        results = solve_optimization_problem(labor, metal, plastic, paint)

        # Выводим результаты
        st.subheader("Оптимальное количество холодильников:")
        st.markdown(f"""
        | **Марка** | **Количество** |
        |:---------:|:--------------:|
        | Марка 1   | {results['x1']} |
        | Марка 2   | {results['x2']} |
        | Марка 3   | {results['x3']} |
        | Марка 4   | {results['x4']} |
        | Марка 5   | {results['x5']} |
        """)

        st.subheader(f"Максимальная прибыль:\n :green[{results['profit']}] р.")