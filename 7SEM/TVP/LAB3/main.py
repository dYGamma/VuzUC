import re

# Получение индекса переменной в строке
def get_index(found_variables, ch):
    return found_variables.find(ch)

# Проверка корректности входных данных
def is_input_correct(function, alphabet, variables, axioms, left_rules, right_rules):
    def check_symbols(s):
        for character in s:
            if character not in alphabet:
                print(f"Ошибка: символ '{character}' не входит в алфавит!")
                return False
        return True

    if not check_symbols(function) or not check_symbols(axioms):
        return False

    for rule in left_rules:
        for character in rule:
            if character not in variables and character not in alphabet:
                print(f"Ошибка: символ '{character}' не входит в алфавит или множество переменных!")
                return False

    return True

# Чтение и разбор входных данных из файла
def read_input(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as fi:
            function = fi.readline().strip()
            alphabet = fi.readline().strip()
            variables = fi.readline().strip()
            axioms = fi.readline().strip()

            # Очистка данных
            def clean_input(s, prefix, suffix):
                return s[len(prefix):-len(suffix)].replace(',', '')

            alphabet = clean_input(alphabet, "A={", "};")
            variables = clean_input(variables, "X={", "};")
            axioms = clean_input(axioms, "A1={", "};")

            # Считывание правил преобразований
            left_rules, right_rules = [], []
            for line in fi:
                line = line.strip()
                if line == "}":
                    break
                if "->" in line:
                    pos = line.find("->")
                    left_rules.append(line[:pos])
                    right_rules.append(line[pos + 2:])

            if left_rules:
                left_rules[0] = left_rules[0][3:]
            if right_rules:
                right_rules[-1] = right_rules[-1][:-1]

            return function, alphabet, variables, axioms, left_rules, right_rules
    except FileNotFoundError:
        print("Ошибка открытия файла!")
        return None

# Функция для применения правил
def apply_rules(function, variables, left_rules, right_rules):
    try:
        with open("D:/GIT/VuzUC/7SEM/TVP/LAB3/output.txt", "w", encoding="utf-8") as out:
            rule_counter = 0
            return_flag = 0
            found_variables = ""

            while return_flag < len(left_rules):
                reg_ex = ""
                found_variables = ""

                for ch in left_rules[rule_counter]:
                    if ch in variables:
                        if ch not in found_variables:
                            reg_ex += "(1*)"
                            found_variables += ch
                        else:
                            reg_ex += f"(\\{get_index(found_variables, ch) + 1})"
                    elif ch in "+=":
                        reg_ex += re.escape(ch)
                    else:
                        reg_ex += ch

                match = re.search(reg_ex, function)
                if match:
                    out.write(f"Исходная строка: {function}\n")
                    out.write(f"Применяемое правило: {left_rules[rule_counter]} -> {right_rules[rule_counter]}\n")

                    return_flag = 0
                    tmp = ""
                    values = [match.group(i) for i in range(1, len(match.groups()) + 1)]

                    for ch in right_rules[rule_counter]:
                        if ch in variables:
                            tmp += values[get_index(found_variables, ch)]
                        else:
                            tmp += ch

                    function = match.string[:match.start()] + tmp + match.string[match.end():]
                    out.write(f"Результат применения правила: {function}\n\n")
                else:
                    return_flag += 1

                rule_counter = (rule_counter + 1) % len(left_rules)

            print("Вычисления завершены")
    except IOError:
        print("Ошибка открытия файла для записи!")

# Главная функция
if __name__ == "__main__":
    # Инициализация переменных
    data = read_input("D:/GIT/VuzUC/7SEM/TVP/LAB3/input.txt")
    if data:
        function, alphabet, variables, axioms, left_rules, right_rules = data
        if is_input_correct(function, alphabet, variables, axioms, left_rules, right_rules):
            apply_rules(function, variables, left_rules, right_rules)
