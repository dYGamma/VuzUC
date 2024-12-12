#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <Windows.h>
#include <algorithm>

using namespace std;

// Получение индекса переменной в строке
// Функция возвращает индекс первого вхождения символа ch в строке found_variables
int get_index(const string& found_variables, char ch) {
    return found_variables.find(ch);
}

// Проверка корректности входных данных
// Проверяется, содержатся ли символы функции, алфавита, переменных, аксиом и правил в допустимых множествах
bool is_input_correct(const string& function, const string& alphabet, const string& variables, const string& axioms, const vector<string>& left_rules, const vector<string>& right_rules) {
    // Локальная лямбда-функция для проверки строки на допустимые символы
    auto check_symbols = [&](const string& str) {
        for (char character : str) {
            if (alphabet.find(character) == string::npos) {
                cout << "Ошибка: символ '" << character << "' не входит в алфавит!" << endl;
                return false;
            }
        }
        return true;
    };

    // Проверка символов в функции и аксиомах
    if (!check_symbols(function) || !check_symbols(axioms)) return false;

    // Проверка символов в правилах
    for (const string& rule : left_rules) {
        for (char character : rule) {
            if (variables.find(character) == string::npos && alphabet.find(character) == string::npos) {
                cout << "Ошибка: символ '" << character << "' не входит в алфавит или множество переменных!" << endl;
                return false;
            }
        }
    }
    return true;
}

// Чтение и разбор входных данных из файла
// Считывает данные из файла и инициализирует входные переменные
bool read_input(const string& filename, string& function, string& alphabet, string& variables, string& axioms, vector<string>& left_rules, vector<string>& right_rules) {
    ifstream fi(filename);
    if (!fi.is_open()) {
        cout << "Ошибка открытия файла!" << endl;
        return false;
    }

    // Считывание основных строк: функции, алфавита, переменных, аксиом
    getline(fi, function);
    getline(fi, alphabet);
    getline(fi, variables);
    getline(fi, axioms);

    // Лямбда-функция для удаления префиксов, суффиксов и лишних символов
    auto clean_input = [](string& str, const string& prefix, const string& suffix) {
        str.erase(0, prefix.size());
        str.erase(str.size() - suffix.size());
        str.erase(remove(str.begin(), str.end(), ','), str.end());
    };

    // Очистка данных
    clean_input(alphabet, "A={", "};");
    clean_input(variables, "X={", "};");
    clean_input(axioms, "A1={", "};");

    // Считывание правил преобразований
    string line;
    while (getline(fi, line) && line != "}") {
        size_t pos = line.find("->");
        if (pos != string::npos) {
            left_rules.push_back(line.substr(0, pos));
            right_rules.push_back(line.substr(pos + 2));
        }
    }

    // Очистка символов из первой и последней строки правил
    if (!left_rules.empty()) left_rules[0].erase(0, 3);
    if (!right_rules.empty()) right_rules.back().pop_back();

    fi.close();
    return true;
}

// Функция для применения правил
// Заменяет строки в функции на основе заданных правил и записывает результат в файл
void apply_rules(string function, const string& variables, const vector<string>& left_rules, const vector<string>& right_rules) {
    ofstream out("output.txt");
    if (!out.is_open()) {
        cout << "Ошибка открытия файла для записи!" << endl;
        return;
    }

    size_t rule_counter = 0; // Индекс текущего правила
    int return_flag = 0; // Счётчик пропущенных правил
    string found_variables; // Найденные переменные для текущего правила

    // Применение правил, пока не будет пройдена вся таблица
    while (return_flag < left_rules.size()) {
        string reg_ex; // Регулярное выражение для текущего правила
        found_variables.clear();

        // Построение регулярного выражения на основе левой части правила
        for (char ch : left_rules[rule_counter]) {
            if (variables.find(ch) != string::npos) {
                // Если переменная новая, добавляется новый захват
                if (get_index(found_variables, ch) == string::npos) {
                    reg_ex += "(1*)";
                    found_variables += ch;
                } else {
                    reg_ex += "(\\" + to_string(get_index(found_variables, ch) + 1) + ')';
                }
            } else if (ch == '+' || ch == '=') {
                reg_ex += "\\" + string(1, ch); // Обработка специальных символов
            } else {
                reg_ex += ch; // Добавление обычного символа
            }
        }

        regex re(reg_ex); // Создание регулярного выражения
        smatch match; // Для хранения результата сопоставления
        if (regex_search(function, match, re)) {
            // Если правило применимо, записываем результат в файл
            out << "Исходная строка: " << function << endl;
            out << "Применяемое правило: " << left_rules[rule_counter] << " -> " << right_rules[rule_counter] << endl;

            return_flag = 0; // Сбрасываем счётчик пропущенных правил
            string tmp; // Буфер для формирования результата
            vector<string> values(match.size() - 1); // Сохранение значений переменных
            for (size_t i = 1; i < match.size(); ++i) {
                values[i - 1] = match[i];
            }

            // Преобразование по правой части правила
            for (char ch : right_rules[rule_counter]) {
                if (variables.find(ch) != string::npos) {
                    tmp += values[get_index(found_variables, ch)];
                } else {
                    tmp += ch;
                }
            }

            // Замена функции на результат
            function = match.prefix().str() + tmp + match.suffix().str();
            out << "Результат применения правила: " << function << endl << endl;
        } else {
            return_flag++; // Увеличиваем счётчик пропущенных правил
        }

        // Переход к следующему правилу
        rule_counter = (rule_counter + 1) % left_rules.size();
    }

    cout << "Вычисления завершены" << endl;
    out.close();
}

int main() {
    SetConsoleOutputCP(1251); // Установка кодировки консоли для корректного отображения русского текста

    // Инициализация переменных
    string function, alphabet, variables, axioms;
    vector<string> left_rules, right_rules;

    // Чтение данных и выполнение правил, если входные данные корректны
    if (read_input("input.txt", function, alphabet, variables, axioms, left_rules, right_rules) &&
        is_input_correct(function, alphabet, variables, axioms, left_rules, right_rules)) {
        apply_rules(function, variables, left_rules, right_rules);
    }

    return 0;
}
