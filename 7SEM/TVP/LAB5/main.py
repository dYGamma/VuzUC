import os
import re
from typing import List

class Row:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.place = []

def read_file(file_name: str) -> str:
    with open(file_name, 'r') as file:
        return file.read()

def write_to_file(cell, r_of_table, c_of_table, correct):
    with open("D:/GIT/VuzUC/7SEM/TVP/LAB5/result.txt", 'w') as file:
        file.write('\t' + '\t'.join(map(str, range(len(c_of_table)))) + '\n')
        for i, row in enumerate(r_of_table):
            file.write(row.symbol + '\t')
            for j in range(len(c_of_table)):
                if not cell[i][j]:
                    file.write('-\t')
                else:
                    col_index = c_of_table.index(cell[i][j])
                    file.write(f"{col_index}/{'1' if correct[col_index] else '0'}\t")
            file.write('\n')

def closing_bracket(string: str, begin: int) -> int:
    stack = []
    for i in range(begin, len(string)):
        if string[i] in "<(":
            stack.append(string[i])
        elif string[i] in ">)":
            stack.pop()
            if not stack:
                return i
    return -1

def find_row(rows: List[Row], char: str) -> int:
    for index, row in enumerate(rows):
        if row.symbol == char:
            return index
    return -1

def markdown(delimiter, string, begin, end, count, rows):
    d_member_b = []
    d_member_e = []
    for i in range(begin, end):
        if i == begin:
            if i == 0:
                delimiter[0].append(0)
                if string[0] not in "<>()|":
                    d_member_b.append(0)
            else:
                delimiter[i].extend(delimiter[i - 1])
                d_member_b.append(i)
        if string[i] not in "<>()|":
            check = find_row(rows, string[i])
            if check == -1:
                rows.append(Row(string[i]))
                rows[-1].place.append(i)
            else:
                rows[check].place.append(i)
            delimiter[i + 1].append(count[0])
            count[0] += 1
        if i > 0 and string[i] not in ">)|" and string[i - 1] == '|':
            delimiter[i].extend(delimiter[begin - 1] if begin else delimiter[begin])
            d_member_b.append(i)
            d_member_e.append(i - 1)
        if i == end - 1:
            if string[end - 1] in ")>":
                d_member_e.append(end - 1)
            for j in d_member_e:
                delimiter[end].extend(delimiter[j])
            if string[end - 1] == '>':
                delimiter[end].extend([x for x in delimiter[begin - 1] if x not in delimiter[end]])
                for j in d_member_b:
                    for k in delimiter[end]:
                        if k not in delimiter[j]:
                            delimiter[j].append(k)
    for i in range(begin, end):
        if string[i] in "<(":
            z_sc = closing_bracket(string, i)
            markdown(delimiter, string, i + 1, z_sc + 1, count, rows)
            i = z_sc

def automaton(cell, r_of_table, c_of_table, delimiter, correct):
    column = 0
    while column < len(c_of_table):
        for state in c_of_table[column]:
            if state in delimiter[-1]:
                correct[column] = True
                break
        for i, row in enumerate(r_of_table):
            cell[i].append([])
            for place in row.place:
                for col_state in c_of_table[column]:
                    if col_state in delimiter[place] and delimiter[place + 1][0] not in cell[i][column]:
                        cell[i][column].append(delimiter[place + 1][0])
            cell[i][column].sort()
            if cell[i][column] not in c_of_table and cell[i][column]:
                c_of_table.append(cell[i][column])
                correct.append(False)
        column += 1

def main():
    string = read_file("D:/GIT/VuzUC/7SEM/TVP/LAB5/input.txt")
    delimiter = [[] for _ in range(len(string) + 1)]
    count = [1]
    r_of_table = []
    c_of_table = [[0]]
    correct = [False]

    markdown(delimiter, string, 0, len(string), count, r_of_table)

    cell = [[[] for _ in range(len(c_of_table))] for _ in range(len(r_of_table))]
    automaton(cell, r_of_table, c_of_table, delimiter, correct)

    write_to_file(cell, r_of_table, c_of_table, correct)

if __name__ == "__main__":
    main()
