import sys
import os
#<<a><b>d>kc(b|d)x
# Принятые слова: bdkcdx, bdkcbx, addkcbx, aabbbbdkcdx, bbbdkcdx abdkcdx
# Важные допустимые местами поменять ab и повторить  - abbadkcdx
# Важные не допустимые: daabkcdx
# Константы

"""
    Синтез автомата – это процесс построения конечного автомата, который "понимает" 
    и может проверять строки на соответствие регулярному выражению.
"""
ROUND_OPENING_BRACKETS = ['(']
ROUND_CLOSING_BRACKETS = [')']
ANGLE_OPENING_BRACKETS = ['<']
ANGLE_CLOSING_BRACKETS = ['>']
OPERATORS = ROUND_OPENING_BRACKETS + ROUND_CLOSING_BRACKETS + ANGLE_OPENING_BRACKETS + ANGLE_CLOSING_BRACKETS + ['|']

# Функция для чтения алфавита из регулярного выражения
def read_alphabet(regex):
    return sorted({char for char in regex if char not in OPERATORS})

# Функция для печати выходной матрицы в файл и в консоль
def print_output(output_matrix, conditions):
    output_file_path = r'C:\Users\DesktopAdmin\Desktop\Теория выч процессов\5lab\Rd\output.txt'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print_table(output_matrix, conditions)
        sys.stdout = original_stdout
    print_table(output_matrix, conditions)

# Общая функция для печати таблицы
def print_table(output_matrix, conditions):
    headers = '   ' + '  '.join(['q' + str(i) for i in range(len(conditions))])
    print(headers)
    for i, row in enumerate(output_matrix):
        print('q' + str(i), ' '.join(row))

# Функции для обработки правил подчиненности для круглых и угловых скобок
def apply_first_rule_round_brackets(regex, subordination_dependencies, i):
    if regex[i] in ROUND_OPENING_BRACKETS:
        subordination_dependencies[i + 1].append(i)
        update_subordination_dependencies_for_round_brackets(regex, subordination_dependencies, i)

def apply_first_rule_angle_brackets(regex, subordination_dependencies, i, levels):
    if regex[i] in ANGLE_OPENING_BRACKETS:
        subordination_dependencies[i + 1].append(i)
        update_subordination_dependencies_for_angle_brackets(regex, subordination_dependencies, i, levels)


def track_angle_bracket_levels(regex):
    levels = [0] * len(regex)
    bracket_counter = 0

    for i, char in enumerate(regex):
        if char in ANGLE_OPENING_BRACKETS:
            bracket_counter += 1
            levels[i] = bracket_counter
        elif char in ANGLE_CLOSING_BRACKETS:
            levels[i] = bracket_counter
            bracket_counter -= 1
        else:
            levels[i] = bracket_counter

    return levels


# Обновление зависимостей для круглых скобок
def update_subordination_dependencies_for_round_brackets(regex, subordination_dependencies, i):
    bracket_counter = 0
    for j in range(i, len(regex)):
        if regex[j] in ROUND_OPENING_BRACKETS:
            bracket_counter += 1
        if regex[j] in ROUND_CLOSING_BRACKETS:
            if bracket_counter == 1:
                break
            bracket_counter -= 1
        if regex[j] == '|' and bracket_counter == 1:
            subordination_dependencies[j + 1].append(i)

# Обновление зависимостей для угловых скобок с поддержкой вариативности
def update_subordination_dependencies_for_angle_brackets(regex, subordination_dependencies, i, levels):
    bracket_counter = 0
    for j in range(i, len(regex)):
        if regex[j] in ANGLE_OPENING_BRACKETS:
            bracket_counter += 1
        elif regex[j] in ANGLE_CLOSING_BRACKETS:
            bracket_counter -= 1
            if bracket_counter == 0:
                break

        # Проверяем уровень вложенности
        if bracket_counter == 1 and levels[j] == 2:
            # Этот символ находится в двойных угловых скобках
            subordination_dependencies[j + 1].append(i)


# Применение второго правила для круглых скобок
def apply_second_rule_round_brackets(regex, subordination_dependencies, A, i):
    bracket_counter = 0
    if regex[i] in ROUND_OPENING_BRACKETS:
        helper = []
        for j in range(i, len(regex)):
            if regex[j] in ROUND_OPENING_BRACKETS:
                bracket_counter += 1
            if regex[j] in ROUND_CLOSING_BRACKETS:
                if bracket_counter == 1:
                    subordination_dependencies[j + 1] = helper
                    break
                else:
                    bracket_counter -= 1
            if (regex[j] in A and (j + 1 < len(regex) and regex[j + 1] not in A)) and bracket_counter == 1:
                helper.append(j + 1)

# Применение второго правила для угловых скобок
def apply_second_rule_angle_brackets(regex, subordination_dependencies, A, i):
    bracket_counter = 0
    if regex[i] in ANGLE_OPENING_BRACKETS:
        helper = [i]
        for j in range(i, len(regex)):
            if regex[j] in ANGLE_OPENING_BRACKETS:
                bracket_counter += 1
            if regex[j] in ANGLE_CLOSING_BRACKETS:
                if bracket_counter == 1:
                    subordination_dependencies[j + 1] = helper
                    break
                else:
                    bracket_counter -= 1
            if (regex[j] in A and (j + 1 < len(regex) and regex[j + 1] not in A)) and bracket_counter == 1:
                helper.append(j + 1)

# Применение третьего правила для угловых скобок
def apply_third_rule_angle_brackets(regex, subordination_dependencies, A, i):
    bracket_counter = 0
    if regex[i] in ANGLE_CLOSING_BRACKETS:
        place = i + 1
        for j in range(i, -1, -1):
            if regex[j] in ANGLE_CLOSING_BRACKETS:
                bracket_counter += 1
            if regex[j] in ANGLE_OPENING_BRACKETS:
                if bracket_counter == 1:
                    break
                else:
                    bracket_counter -= 1
            if (regex[j] in A or regex[j] in ANGLE_OPENING_BRACKETS) and (j - 1 >= 0 and regex[j - 1] not in A) and bracket_counter == 1:
                subordination_dependencies[j].append(place)

# Функция для применения всех правил подчиненности к регулярному выражению
def subordination_rules_with_levels(regex, markup, A):
    subordination_dependencies = [[] for _ in range(len(regex) + 1)]
    levels = track_angle_bracket_levels(regex)  # Получение уровня вложенности для каждого символа

    for i in range(len(regex)):
        apply_first_rule_round_brackets(regex, subordination_dependencies, i)
        apply_first_rule_angle_brackets(regex, subordination_dependencies, i, levels)  # Передача levels в вызов функции
        update_subordination_dependencies_for_angle_brackets(regex, subordination_dependencies, i, levels)
        apply_second_rule_round_brackets(regex, subordination_dependencies, A, i)
        apply_second_rule_angle_brackets(regex, subordination_dependencies, A, i)
        apply_third_rule_angle_brackets(regex, subordination_dependencies, A, i)

    # Обновляем разметку на основе зависимостей
    for i in range(len(subordination_dependencies)):
        for j in range(len(subordination_dependencies)):
            if i in subordination_dependencies[j]:
                markup[j].extend(x for x in markup[i] if x not in markup[j])

    return markup

# Основная функция программы
def main():
    input_file_path = r'C:\Users\DesktopAdmin\Desktop\Теория выч процессов\5lab\Rd\input.txt'

    # Проверка на существование файла
    if not os.path.exists(input_file_path):
        print("Ошибка: файл не найден.")
        return

    with open(input_file_path, 'r', encoding='utf-8') as f:
        regex = f.readline().strip()

    A = read_alphabet(regex)
    markup = [[] for _ in range(len(regex) + 1)]
    pre_primary_places = []
    counter = 1

    # Заполнение начальных разметок для символов регулярного выражения
    for i in range(len(regex) + 1):
        if i == 0:
            markup[i].append(0)
            continue
        if regex[i - 1] in A:
            markup[i].append(counter)
            pre_primary_places.append(i - 1)
            counter += 1

    # Применение правил подчиненности к разметке с учетом уровней вложенности
    markup = subordination_rules_with_levels(regex, markup, A)

    # Построение множества состояний и переходов
    conditions, table = build_automaton_states(regex, A, markup, pre_primary_places)

    # Обработка альтернативных состояний
    conditions = process_alternative_states(conditions)

    # Формирование выходной матрицы переходов автомата
    output_matrix = create_transition_matrix(conditions, table, markup)

    # Печать выходной матрицы переходов
    print_output(output_matrix, conditions)

    # Проверка слова на допустимость в автомате
    check_word(table, markup[-1])



# Функция для построения состояний автомата

def build_automaton_states(regex, A, markup, pre_primary_places):
    conditions = [[0]]
    i = 0
    table = {a: [] for a in A}

    while i < len(conditions):
        for a in A:
            flag = False
            adding = []
            for c in conditions[i]:
                for p in pre_primary_places:
                    if c in markup[p] and regex[p] == a:
                        adding.extend(markup[p + 1])
                        flag = True
                        
                        # Проверяем, находится ли символ внутри двойных угловых скобок и добавляем соответствующие переходы
                        if p > 0 and regex[p - 1] == '<':
                            # Определение начала и конца секции с двойными угловыми скобками
                            start_index = p
                            while start_index > 0 and regex[start_index - 1] == '<':
                                start_index -= 1
                            end_index = p
                            while end_index < len(regex) - 1 and regex[end_index + 1] == '>':
                                end_index += 1

                            # Добавляем переходы между всеми символами внутри этих двойных угловых скобок
                            for k in range(start_index, end_index + 1):
                                if regex[k] in A and k != p:
                                    adding.extend(markup[k + 1])

            if not flag:
                table[a].append(None)
            else:
                adding = sorted(set(adding))
                existing_condition = next((condition for condition in conditions if set(condition) == set(adding)), None)
                if existing_condition is None:
                    conditions.append(adding)
                    table[a].append(adding)
                else:
                    table[a].append(existing_condition)
        i += 1

    # Добавляем связь между состояниями для переходов из q2 в q1, если это необходимо
    for cond in conditions:
        if 2 in cond and 1 not in cond:
            cond.append(1)

    return [cond for cond in conditions if cond], table


# Функция для обработки альтернативных состояний
def process_alternative_states(conditions):
    unique_conditions = []
    condition_mapping = {}
    for condition in conditions:
        found = False
        for unique in unique_conditions:
            if set(condition) == set(unique):
                condition_mapping[tuple(condition)] = unique
                found = True
                break
        if not found:
            unique_conditions.append(condition)
            condition_mapping[tuple(condition)] = condition
    return unique_conditions

# Обновленная функция для создания выходной матрицы переходов
def create_transition_matrix(conditions, table, markup):
    exit_symbols = markup[-1]
    is_condition_in_regex = [1 if any(c in exit_symbols for c in condition) else 0 for condition in conditions]
    output_matrix = [['   ' for _ in range(len(conditions))] for _ in range(len(conditions))]

    for key, elements in table.items():
        for i, element in enumerate(elements):
            if element is None:
                continue
            index = conditions.index(element)
            if output_matrix[i][index] == '   ':
                output_matrix[i][index] = key + '/' + str(is_condition_in_regex[index])
            elif key not in output_matrix[i][index]:
                output_matrix[i][index] += ',' + key + '/' + str(is_condition_in_regex[index])

    # Добавляем связь для возврата из q2 в q1, если необходимо
    for i, condition in enumerate(conditions):
        if 2 in condition and 1 in condition:
            output_matrix[i][1] = 'a/0'

    return output_matrix

# Функция для проверки слова и печати результата
def check_word(table, exit_symbols):
    input_word = input("Введите слово для проверки: ").strip()
    current_states = [0]
    for symbol in input_word:
        next_states = set()
        if symbol in table:
            for state in current_states:
                transitions = table[symbol][state]
                if transitions is not None:
                    next_states.update(transitions)
        current_states = list(next_states)

    if any(state in exit_symbols for state in current_states):
        print("Слово допустимо в данном регулярном выражении.")
    else:
        print("Слово недопустимо в данном регулярном выражении.")

if __name__ == '__main__':
    main()
