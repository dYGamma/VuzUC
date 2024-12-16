from graphviz import Digraph

# Создаем объект диаграммы
def create_idef0_diagram():
    diagram = Digraph('IDEF0', format='png')
    diagram.attr(rankdir='TB')

    # Определяем узлы
    diagram.node('A0', 'Система автоматического обнаружения и наведения', shape='box', style='filled', fillcolor='lightblue')
    
    # Входы
    diagram.node('Input1', 'Тепловая матрица (8x8)', shape='ellipse', style='filled', fillcolor='lightyellow')
    diagram.node('Input2', 'Сигнал с сервоприводов', shape='ellipse', style='filled', fillcolor='lightyellow')
    
    # Выходы
    diagram.node('Output1', 'Изображение тепловой карты', shape='ellipse', style='filled', fillcolor='lightgreen')
    diagram.node('Output2', 'Положение камеры', shape='ellipse', style='filled', fillcolor='lightgreen')

    # Управление
    diagram.node('Control1', 'Алгоритм обработки данных', shape='hexagon', style='filled', fillcolor='lightgray')
    diagram.node('Control2', 'Команды от микроконтроллера', shape='hexagon', style='filled', fillcolor='lightgray')

    # Механизмы
    diagram.node('Mechanism1', 'Тепловизор AMG8833', shape='ellipse', style='filled', fillcolor='lightpink')
    diagram.node('Mechanism2', 'Arduino и сервоприводы', shape='ellipse', style='filled', fillcolor='lightpink')
    diagram.node('Mechanism3', 'Дисплей TFT', shape='ellipse', style='filled', fillcolor='lightpink')

    # Добавляем связи
    diagram.edge('Input1', 'A0', label='Входные данные')
    diagram.edge('Input2', 'A0', label='Текущее положение')
    diagram.edge('Control1', 'A0', label='Обработка')
    diagram.edge('Control2', 'A0', label='Управление')
    diagram.edge('A0', 'Output1', label='Результаты отображения')
    diagram.edge('A0', 'Output2', label='Положение камеры')
    diagram.edge('Mechanism1', 'A0', label='Сбор данных')
    diagram.edge('Mechanism2', 'A0', label='Приводы')
    diagram.edge('Mechanism3', 'A0', label='Вывод')

    # Сохраняем диаграмму
    try:
        diagram.render('IDEF0_Diagram', cleanup=True)
    except FileNotFoundError as e:
        print("Ошибка: Graphviz не установлен или недоступен в PATH. Убедитесь, что Graphviz установлен и добавлен в системный PATH.")
        raise e


# Генерация диаграммы
create_idef0_diagram()