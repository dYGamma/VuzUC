import sys  # импортируем модуль sys для работы с системными сообщениями и завершением программы


# класс для реализации машины Тьюринга
class TuringMachine:
    def __init__(self, tape, program, alphabet):
        # инициализация машины Тьюринга
        self.tape = list(tape)  # лента представлена в виде списка символов
        self.head_position = 0  # начальная позиция головки на ленте
        self.state = 'q0'  # начальное состояние
        self.program = program  # программа с командами для машины Тьюринга
        self.alphabet = alphabet  # алфавит допустимых символов
        self.history = []  # история выполнения команд для вывода в файл

    # метод для перемещения головки машины
    def move_head(self, direction):
        if direction == 'R':  # если указано движение вправо
            self.head_position += 1
            # если головка выходит за правый край ленты, расширяем её
            if self.head_position >= len(self.tape):
                self.tape.append('_')  # добавляем пустой символ '_'
        elif direction == 'L':  # если указано движение влево
            self.head_position -= 1
            # если головка выходит за левый край, расширяем ленту слева
            if self.head_position < 0:
                self.tape.insert(0, '_')
                self.head_position = 0  # сдвигаем позицию головки на начало

    # метод выполнения программы машины Тьюринга
    def execute(self):
        # пока текущее состояние не является терминальным ('!')
        while self.state != '!':
            # получаем символ, на котором находится головка
            current_symbol = self.tape[self.head_position]
            # ищем команду для текущего состояния и символа
            command = self.program.get((self.state, current_symbol))

            # если команда не найдена, записываем ошибку и выходим из цикла
            if not command:
                self.history.append(f"Ошибка: нет перехода для ({self.state}, {current_symbol})")
                break

            # распаковываем команду: новый символ, направление движения, новое состояние
            new_symbol, direction, new_state = command

            # записываем текущее состояние ленты и выполняемую команду для истории
            tape_before = ''.join(self.tape)  # состояние ленты перед выполнением команды
            head_pos = ' ' * self.head_position + '^'  # позиция головки на ленте
            command_str = f"{self.state},{current_symbol} -> {new_symbol},{direction},{new_state}"

            # добавляем запись в историю
            self.history.append(f"{tape_before}\n{head_pos}\n{command_str}")

            # выполняем команду: заменяем символ на новый и двигаем головку
            self.tape[self.head_position] = new_symbol
            self.move_head(direction)
            self.state = new_state  # переходим в новое состояние

    # метод для сохранения результата работы в файл
    def save_output(self, filename):
        with open(filename, 'w') as f:
            # записываем историю выполнения команд
            for line in self.history:
                f.write(line + '\n')
            # записываем итоговое состояние ленты
            f.write("Итоговое состояние ленты: " + ''.join(self.tape) + '\n')


# функция для загрузки содержимого файла
def load_file(filename):
    with open(filename, 'r') as f:
        return f.read().strip()  # считываем содержимое и удаляем лишние пробелы


# функция для загрузки программы из файла
def load_program(filename):
    program = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()  # убираем лишние пробелы по краям
            if not line or '->' not in line:
                continue  # пропускаем пустые строки и строки без '->'

            # разделяем строку на левую и правую части по разделителю '->'
            left, right = line.split('->')
            left = left.strip()
            right = right.strip()

            try:
                # разбиваем левую часть на состояние и символ
                state, symbol = left.split(',')
                # разбиваем правую часть на новый символ, направление и новое состояние
                new_symbol, direction, new_state = right.split(',')
                # сохраняем команду в словарь
                program[(state.strip(), symbol.strip())] = (new_symbol.strip(), direction.strip(), new_state.strip())
            except ValueError:
                print(f"Ошибка в строке программы: '{line}'")
                sys.exit(1)  # завершаем выполнение, если ошибка при разборе строки
    return program


# функция для загрузки алфавита из файла
def load_alphabet(filename):
    with open(filename, 'r') as f:
        return set(f.read().strip().split(','))  # считываем и создаём множество символов


# загрузка данных из файлов
tape = load_file('LAB2/tape.txt')  # лента
program = load_program('LAB2/program.txt')  # программа
alphabet = load_alphabet('LAB2/alphabet.txt')  # алфавит

# проверка символов на ленте на принадлежность алфавиту
for symbol in tape:
    if symbol not in alphabet:
        sys.exit(f"Ошибка: символ '{symbol}' не принадлежит алфавиту")

# создание машины Тьюринга и выполнение программы
tm = TuringMachine(tape, program, alphabet)
tm.execute()
tm.save_output('output.txt')  # сохранение результата в файл

print("Выполнение завершено. Результаты сохранены в output.txt.")
