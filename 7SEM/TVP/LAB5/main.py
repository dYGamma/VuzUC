import os
from typing import List

class Row:
    def __init__(self, symbol: str, place: List[int]):
        self.symbol = symbol  # символ регулярного выражения
        self.place = place  # позиции символа в регулярном выражении

def read_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(cell, r_of_table, c_of_table, correct):
    with open("LAB5/result.txt", 'w', encoding='utf-8') as file:
        # Заголовки столбцов
        file.write("\t" + "\t".join(map(str, range(len(c_of_table)))) + "\n")
        
        # Таблица переходов
        for i, row in enumerate(r_of_table):
            file.write(f"{row.symbol}\t")
            for j in range(len(c_of_table)):
                if not cell[i][j]:
                    file.write("-\t")
                else:
                    idx = c_of_table.index(cell[i][j])
                    status = '1' if correct[idx] else '0'
                    file.write(f"{idx}/{status}\t")
            file.write("\n")

def automaton(cell, r_of_table, c_of_table, delimiter, correct):
    column = 0
    while column < len(c_of_table):
        # Проверка конечных состояний
        for i in c_of_table[column]:
            for j in delimiter[-1]:
                if i == j:
                    correct[column] = True
                    break
            if correct[column]:
                break

        for i, row in enumerate(r_of_table):
            cell[i].append([])
            for pos in row.place:
                for k in c_of_table[column]:
                    if k in delimiter[pos] and delimiter[pos + 1][0] not in cell[i][column]:
                        cell[i][column].append(delimiter[pos + 1][0])
            cell[i][column].sort()
            if cell[i][column] and cell[i][column] not in c_of_table:
                c_of_table.append(cell[i][column])
                correct.append(False)
        column += 1

def markdown(delimiter, string, begin, end, count, r_of_table):
    d_member_b, d_member_e = [], []
    for i in range(begin, end):
        if i == begin:
            if i == 0:
                delimiter[0].append(0)
                if string[0] not in "<>()":
                    d_member_b.append(0)
            else:
                delimiter[i] = delimiter[i - 1][:]
                d_member_b.append(i)
        if string[i] not in "<>()|":
            check = next((idx for idx, r in enumerate(r_of_table) if r.symbol == string[i]), -1)
            if check == -1:
                r_of_table.append(Row(string[i], [i]))
            else:
                r_of_table[check].place.append(i)
            delimiter[i + 1].append(count)
            count += 1

        if i > 0 and string[i] not in ">|" and string[i - 1] == "|":
            delimiter[i].extend(delimiter[begin - 1] if begin else delimiter[begin])
            d_member_b.append(i)
            d_member_e.append(i - 1)

        if i == end - 1:
            if string[end - 1] in ")>":
                d_member_e.append(end - 1)
            for j in d_member_e:
                delimiter[end].extend(delimiter[j])
            if string[end - 1] == ">":
                delimiter[end].extend(set(delimiter[begin - 1]) - set(delimiter[end]))
                for j in d_member_b:
                    delimiter[j].extend(set(delimiter[end]) - set(delimiter[j]))
                    if string[j] in "<(":
                        dop(delimiter, string, j + 1, closing_bracket(string, j))

        if string[i] in "<(":
            z_sc = closing_bracket(string, i)
            markdown(delimiter, string, i + 1, z_sc + 1, count, r_of_table)
            i = z_sc

def dop(delimiter, string, begin, end):
    for i in range(begin, end):
        if string[i] not in "<>()|":
            delimiter[i + 1].extend(delimiter[i])

def closing_bracket(string, begin):
    stack = 1
    for i in range(begin + 1, len(string)):
        if string[i] in "<(":
            stack += 1
        elif string[i] in ">)":
            stack -= 1
        if stack == 0:
            return i
    return -1

def main():
    string = read_file("LAB5/input.txt")
    delimiter = [[] for _ in range(len(string) + 1)]
    count = 1
    r_of_table = []
    c_of_table = [[0]]
    correct = [False]

    markdown(delimiter, string, 0, len(string), count, r_of_table)
    cell = [[[] for _ in range(len(c_of_table))] for _ in range(len(r_of_table))]
    automaton(cell, r_of_table, c_of_table, delimiter, correct)
    write_to_file(cell, r_of_table, c_of_table, correct)

if __name__ == "__main__":
    main()
