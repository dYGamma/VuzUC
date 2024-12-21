import os

class Row:
    def __init__(self, symbol, place=None):
        self.symbol = symbol  # символ регулярного выражения
        self.place = place if place else []  # позиции символа в регулярном выражении


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.readline().strip()
            if not content:
                print("Файл пуст!")
            return content
    except FileNotFoundError:
        print("Файл не может быть открыт!")
        return ""


def write_to_file(cell, r_of_table, c_of_table, correct):
    with open("result.txt", "w", encoding="utf-8") as file:
        # Запись заголовков столбцов
        for i in range(len(c_of_table)):
            file.write(f'\t{i}')
        
        # Запись таблицы переходов
        for i, row in enumerate(r_of_table):
            file.write(f'\n{row.symbol}\t')
            for j in range(len(c_of_table)):
                if not cell[i][j]:
                    file.write("-\t")
                else:
                    col_index = c_of_table.index(cell[i][j])
                    file.write(f"{col_index}/{'1' if correct[col_index] else '0'}\t")


def closing_bracket(string, begin):
    count = 1
    brackets = "<>" if string[begin] == '<' else "()"
    while True:
        begin += 1
        if string[begin] == brackets[0]:
            count += 1
        elif string[begin] == brackets[1]:
            count -= 1
            if count == 0:
                return begin  # Возвращаем индекс закрывающей скобки


def markdown(delimiter, string, begin, end, count, r_of_table):
    d_member_b = []
    d_member_e = []

    for i in range(begin, end):
        if i == begin:
            if i == 0:
                delimiter[0].append(0)
                if string[0] not in "<>()":
                    d_member_b.append(0)
            else:
                delimiter[i].extend(delimiter[i - 1])
                d_member_b.append(i)

        if string[i] not in "<>()|":
            check = find_row(r_of_table, string[i])
            if check == -1:
                r_of_table.append(Row(string[i], [i]))
            else:
                r_of_table[check].place.append(i)
            delimiter[i + 1].append(count)
            count += 1

        if i > 0 and string[i - 1] == "|" and string[i] not in ">|)":
            delimiter[i].extend(delimiter[begin if begin == 0 else begin - 1])
            d_member_b.append(i)
            d_member_e.append(i - 1)

        if i == end - 1:
            if string[end - 1] in ")>":
                d_member_e.append(end - 1)
            for j in d_member_e:
                delimiter[end].extend(delimiter[j])
            if string[end - 1] == '>':
                delimiter[end].extend(delimiter[begin - 1])
                for b in d_member_b:
                    delimiter[b].extend(delimiter[end])
                    if string[b] in "<(":
                        dop(delimiter, string, b + 1, closing_bracket(string, b))

        if string[i] in "<(":
            z_sc = closing_bracket(string, i)
            markdown(delimiter, string, i + 1, z_sc + 1, count, r_of_table)
            i = z_sc


def dop(delimiter, string, begin, end):
    for i in range(begin, end):
        if i == begin:
            delimiter[begin].extend(delimiter[begin - 1])
        if string[i] == "|" and string[i - 1] in "<(":
            dop(delimiter, string, i + 1, closing_bracket(string, i))
        if string[i] in "<(":
            z_sc = closing_bracket(string, i)
            dop(delimiter, string, i + 1, z_sc)
            i = z_sc


def find_row(rows, char):
    for i, row in enumerate(rows):
        if row.symbol == char:
            return i
    return -1


def automaton(cell, r_of_table, c_of_table, delimiter, correct):
    column = 0
    while column < len(c_of_table):
        for c in c_of_table[column]:
            if c in delimiter[-1]:
                correct[column] = True

        for i, row in enumerate(r_of_table):
            cell[i].append([])
            for place in row.place:
                for col in c_of_table[column]:
                    if col in delimiter[place] and delimiter[place + 1][0] not in cell[i][column]:
                        cell[i][column].append(delimiter[place + 1][0])
            cell[i][column].sort()

            if cell[i][column] and cell[i][column] not in c_of_table:
                c_of_table.append(cell[i][column])
                correct.append(False)
        column += 1


def main():
    string = read_file("LAB5/input.txt")
    if not string:
        return

    delimiter = [[] for _ in range(len(string) + 1)]
    count = 1
    r_of_table = []
    correct = []
    c_of_table = [[0]]
    correct.append(False)

    markdown(delimiter, string, 0, len(string), count, r_of_table)
    cell = [[[] for _ in range(len(c_of_table))] for _ in range(len(r_of_table))]
    automaton(cell, r_of_table, c_of_table, delimiter, correct)

    write_to_file(cell, r_of_table, c_of_table, correct)
    os.system("pause")


if __name__ == "__main__":
    main()
