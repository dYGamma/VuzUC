import sys
from typing import List, Tuple

class Row:
    def __init__(self, symbol: str):
        self.symbol = symbol  # символ регулярного выражения
        self.place = []  # позиции символа в регулярном выражении

def read_file(filename: str) -> str:
    """Считывает содержимое файла и возвращает строку."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_to_file(cell, rows, column_headers, correct):
    """Записывает таблицу переходов в файл result.txt."""
    with open("result.txt", "w", encoding="utf-8") as file:
        # Заголовки столбцов
        file.write("\t" + "\t".join([f"q{i}" for i in range(len(column_headers))]) + "\n")

        # Запись таблицы переходов
        for i, row in enumerate(rows):
            file.write(f"{row.symbol}\t")
            for j, column in enumerate(column_headers):
                if not cell[i][j]:
                    file.write("-\t")
                else:
                    idx = column_headers.index(cell[i][j])
                    status = '1' if correct[idx] else '0'
                    file.write(f"q{idx}/{status}\t")
            file.write("\n")

def find_row(rows: List[Row], symbol: str) -> int:
    """Ищет символ в списке заголовков строк и возвращает его индекс."""
    for i, row in enumerate(rows):
        if row.symbol == symbol:
            return i
    return -1

def closing_bracket(s: str, begin: int) -> int:
    """Находит закрывающую скобку для текущей позиции."""
    stack = 0
    for i in range(begin, len(s)):
        if s[i] in '(<':
            stack += 1
        elif s[i] in ')>':
            stack -= 1
            if stack == 0:
                return i
    return -1

def dop(delimiter: List[List[int]], s: str, begin: int, end: int):
    for i in range(begin, end):
        if i == begin:
            for idx in delimiter[begin - 1]:
                if idx not in delimiter[begin]:
                    delimiter[begin].append(idx)

def markdown(delimiter: List[List[int]], s: str, begin: int, end: int, count: int, rows: List[Row]):
    d_member_b = []
    d_member_e = []

    i = begin
    while i < end:
        if i == begin:
            if i == 0:
                delimiter[0].append(0)
                if s[0] not in '<>()':
                    d_member_b.append(0)
            else:
                delimiter[i] += delimiter[i - 1]
                d_member_b.append(i)

        if s[i] not in '<>()|':
            idx = find_row(rows, s[i])
            if idx == -1:
                rows.append(Row(s[i]))
                rows[-1].place.append(i)
            else:
                rows[idx].place.append(i)
            delimiter[i + 1].append(count)
            count += 1

        if i > 0 and s[i - 1] == '|':
            delimiter[i] += delimiter[begin - 1] if begin else delimiter[begin]
            d_member_b.append(i)
            d_member_e.append(i - 1)

        if i == end - 1:
            if s[end - 1] in '>)':
                d_member_e.append(end - 1)
            for j in d_member_e:
                delimiter[end] += delimiter[j]
            if s[end - 1] == '>':
                for j in d_member_b:
                    dop(delimiter, s, j + 1, closing_bracket(s, j))

        if s[i] in '(<':
            z_sc = closing_bracket(s, i)
            markdown(delimiter, s, i + 1, z_sc + 1, count, rows)
            i = z_sc
        i += 1

def automaton(cell, rows: List[Row], column_headers, delimiter: List[List[int]], correct: List[bool]):
    column = 0
    while column < len(column_headers):
        for state in column_headers[column]:
            if state in delimiter[-1]:
                correct[column] = True
                break

        for i, row in enumerate(rows):
            cell[i].append([])
            for place in row.place:
                for state in column_headers[column]:
                    if state in delimiter[place] and delimiter[place + 1][0] not in cell[i][column]:
                        cell[i][column].append(delimiter[place + 1][0])

            cell[i][column].sort()
            if cell[i][column] not in column_headers and cell[i][column]:
                column_headers.append(cell[i][column])
                correct.append(False)
        column += 1

def main():
    s = read_file("LAB5\input.txt")
    delimiter = [[] for _ in range(len(s) + 1)]
    count = 1
    rows = []
    correct = [False]
    column_headers = [[0]]
    
    markdown(delimiter, s, 0, len(s), count, rows)
    cell = [[[] for _ in range(len(column_headers))] for _ in range(len(rows))]
    automaton(cell, rows, column_headers, delimiter, correct)
    write_to_file(cell, rows, column_headers, correct)

if __name__ == "__main__":
    main()
