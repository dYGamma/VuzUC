#include <iostream>    // Подключение библиотеки для работы с потоками ввода-вывода
#include <deque>       // Подключение библиотеки для работы с двусторонними очередями
#include <sstream>     // Подключение библиотеки для работы с потоками строк
#include <string>      // Подключение библиотеки для работы со строками
#include <vector>      // Подключение библиотеки для работы с динамическими массивами (векторами)
#include <algorithm>   // Подключение библиотеки для работы с алгоритмами (например, для поиска)

#include "lab4.h"      // Подключение пользовательского заголовочного файла (неизвестно, что именно он содержит)

static int const tableSize = 5;      // Определение константы размера таблицы (размер кэша) равной 5

static int actualFifoRow = 0;        // Переменная для отслеживания текущей строки в FIFO алгоритме

static int systemCounter = 0;        // Счётчик системного времени для отслеживания времени работы алгоритма

bool debug = false;                  // Переменная для включения/выключения режима отладки

// Структура для представления строки таблицы FIFO
struct FIFORow {
    int vpn = -1;                     // vpn инициализируется значением -1, что означает "пустое место"
};
std::deque<FIFORow> fifoTable(tableSize);  // Создание двусторонней очереди фиксированного размера tableSize для хранения страниц

// Функция для печати состояния таблицы FIFO
void printFifoTable() {
    for (int i = 0; i < tableSize; ++i) {           // Проход по всем элементам таблицы
        if (fifoTable[i].vpn != -1) {               // Если vpn не равен -1, значит это занятое место
            std::cout << fifoTable[i].vpn;         // Вывод vpn
        } else {
            std::cout << "#";                     // Вывод "#" для пустого места
        }
        if (i < tableSize - 1) {                    // Если это не последний элемент, добавляем пробел
            std::cout << " ";
        }
    }
    std::cout << "\n";                             // Печать новой строки после окончания строки таблицы
}

// Функция для проверки наличия страницы в таблице FIFO
bool checkFifoTable(int vpn) {
    for (auto &row : fifoTable) {                  // Перебор всех элементов таблицы
        if (row.vpn == vpn) {                      // Если vpn уже присутствует
            return false;                         // Возвращаем false, так как страница уже есть
        }
    }
    return true;                                  // Возвращаем true, если страница не найдена
}

// Реализация алгоритма FIFO
void fifoAlg() {
    std::string input;                            // Строка для хранения входных данных
    int command = 0;                             // Переменная для хранения команды
    int vpn = 0;                                 // Переменная для хранения vpn

    while (true) {                               // Бесконечный цикл обработки входных данных
        std::getline(std::cin, input);          // Чтение строки из стандартного ввода
        if (input.empty()) {                    // Если строка пуста, выходим из цикла
            return;
        }
        std::istringstream istream{ input };    // Создание строки потока для разбора входных данных
        if (!(istream >> command) || !(istream >> vpn) || istream >> input) {
            continue;                          // Если входные данные не удалось разобрать, переходим к следующей итерации
        }

        if (checkFifoTable(vpn)) {              // Проверка, существует ли vpn в таблице
            fifoTable[(actualFifoRow % tableSize)].vpn = vpn; // Запись vpn в текущую строку таблицы FIFO
            actualFifoRow++;                   // Переход к следующей строке
        }
        printFifoTable();                      // Печать текущего состояния таблицы FIFO
    }
}

// Структура для представления строки таблицы Working Set
struct WSRow {
    int vpn;              // Номер виртуальной страницы
    bool flagR;          // Флаг чтения
    bool flagM;          // Флаг модификации
    int systemTime;      // Время последнего доступа
};
std::vector<WSRow> wsTable;  // Вектор для хранения строк таблицы Working Set

// Функция для проверки наличия страницы в таблице Working Set и обновления её состояния
bool checkWSTable(int vpn, int command) {
    for (auto &row : wsTable) {                // Перебор всех элементов таблицы
        if (row.vpn == vpn) {                  // Если vpn уже присутствует
            row.flagR = true;                 // Обновление флага чтения
            row.flagM = command;              // Обновление флага модификации в зависимости от команды
            return false;                     // Возвращаем false, так как страница уже есть
        }
    }
    return true;                              // Возвращаем true, если страница не найдена
}

// Реализация алгоритма Working Set
void wsAlgImplementation(int command, int vpn) {

    if (!checkWSTable(vpn, command)) {         // Проверка и обновление таблицы Working Set
        if (debug)
            std::cout << "page : " << vpn << " time : " << systemCounter << "\n";
        return;                               // Если страница уже в таблице, ничего не делаем
    }

    for (auto &row : wsTable) {                // Обновление времени доступа для всех страниц с флагом чтения
        if (row.flagR) {
            row.systemTime = systemCounter;    // Обновление времени последнего доступа
        }
    }

    bool isFlagM = command == 1;               // Установка флага модификации в зависимости от команды

    if (wsTable.size() != tableSize)           // Если размер таблицы меньше максимального
    {
        wsTable.push_back({vpn, true, isFlagM, systemCounter}); // Добавление новой страницы в таблицу
        return;
    }

    auto notNullAgeIter = std::find_if(std::begin(wsTable), std::end(wsTable), [](WSRow page) {
        return page.systemTime != systemCounter;  // Поиск страницы, время доступа которой не совпадает с текущим временем
    });

    if (notNullAgeIter == std::end(wsTable))    // Если не найдена страница с устаревшим временем доступа
    {
        std::vector<int> indexesVec;
        for (int i = 0; i < tableSize; ++i) {  // Заполнение вектора индексами страниц без флага модификации
            if (!wsTable.at(i).flagM)
                indexesVec.push_back(i);
        }

        if (!indexesVec.empty()) {             // Если есть страницы без модификаций
            int index = uniform_rnd(0, indexesVec.size() - 1); // Выбор случайного индекса
            wsTable[indexesVec.at(index)] = {vpn, true, isFlagM, systemCounter}; // Замена выбранной страницы
            return;
        }

        wsTable[uniform_rnd(0, wsTable.size() - 1)] = {vpn, true, isFlagM, systemCounter}; // Замена случайной страницы
        return;
    }

    std::vector<int> oldestPagesIndexes;         // Вектор для хранения индексов страниц с наименьшим возрастом
    std::vector<int> oldestPagesIndexesNotModifyed; // Вектор для хранения индексов страниц с наименьшим возрастом и без модификаций
    int oldestAge = 0;
    for (int i = 0; i < tableSize; ++i) {
        int age = systemCounter - wsTable[i].systemTime; // Вычисление возраста страницы
        if (age == oldestAge) {
            if (!wsTable[i].flagM)
                oldestPagesIndexesNotModifyed.push_back(i);
            else
                oldestPagesIndexes.push_back(i);
            continue;
        }

        if (age > oldestAge) {
            oldestAge = age;
            oldestPagesIndexes.clear();
            oldestPagesIndexesNotModifyed.clear();
            if (!wsTable[i].flagM)
                oldestPagesIndexesNotModifyed.push_back(i);
            else
                oldestPagesIndexes.push_back(i);
            continue;
        }
    }

    int index = 0;
    if (!oldestPagesIndexesNotModifyed.empty()) {
        index = uniform_rnd(0, oldestPagesIndexesNotModifyed.size() - 1); // Выбор случайной страницы из не модифицированных
        wsTable[oldestPagesIndexesNotModifyed.at(index)] = {vpn, true, isFlagM, systemCounter}; // Замена страницы
        return;
    }

    index = uniform_rnd(0, oldestPagesIndexes.size() - 1); // Выбор случайной страницы из старейших
    wsTable[oldestPagesIndexes.at(index)] = {vpn, true, isFlagM, systemCounter}; // Замена страницы
}

// Функция для печати состояния таблицы Working Set
void printWSTable() {
    for (int i = 0; i < tableSize; ++i) {                // Проход по всем элементам таблицы
        if (i < wsTable.size()) {
            if (debug)
                std::cout << wsTable[i].vpn << "(" << wsTable[i].flagR << "," << wsTable[i].flagM << "," << wsTable[i].systemTime << ")";
            else
                std::cout << wsTable[i].vpn;
        } else {
            std::cout << "#";                           // Вывод "#" для пустого места
        }
        if (i < tableSize - 1) {                        // Если это не последний элемент, добавляем пробел
            std::cout << " ";
        }
    }
    std::cout << "\n";                                 // Печать новой строки после окончания строки таблицы
}

// Реализация алгоритма Working Set
void wsAlgo() {
    std::string input;                                // Строка для хранения входных данных
    int command = 0;                                 // Переменная для хранения команды
    int vpn = 0;                                     // Переменная для хранения vpn

    while (true) {                                   // Бесконечный цикл обработки входных данных
        std::getline(std::cin, input);              // Чтение строки из стандартного ввода
        if (input.empty()) {                        // Если строка пуста, выходим из цикла
            return;
        }
        std::istringstream istream{ input };        // Создание строки потока для разбора входных данных
        if (!(istream >> command) || !(istream >> vpn) || istream >> input) {
            continue;                              // Если входные данные не удалось разобрать, переходим к следующей итерации
        }

        wsAlgImplementation(command, vpn);         // Выполнение алгоритма Working Set
        systemCounter++;                           // Увеличение системного времени
        if (systemCounter % 5 == 0) {              // Каждые 5 единиц времени
            for (auto &virtualPage : wsTable) {
                virtualPage.flagR = 0;             // Сброс флага чтения для всех страниц
            }
        }

        printWSTable();                          // Печать текущего состояния таблицы Working Set
    }
}

// Основная функция программы
int main(int argc, char *argv[]) {
    switch (atoi(argv[1])) {                      // Чтение первого аргумента командной строки
    case 1:                                      // Если аргумент равен 1, выполняется алгоритм FIFO
    {
        fifoAlg();
        break;
    }
    case 2:                                      // Если аргумент равен 2, выполняется алгоритм Working Set
    {
        wsAlgo();
        break;
    }
    default:
        break;
    }

    return 0;                                   // Возврат к операционной системе
}



Алгоритмы
FIFO (First-In-First-Out)
Описание: FIFO — это алгоритм замены страниц в операционных системах, при котором страница, которая находилась в памяти дольше всего, заменяется первой. 
Это напоминает очередь: первой зашедшей страницей будет та, которая выйдет первой.
Применение: В данном коде FIFO реализован с использованием двусторонней очереди std::deque. 
Когда требуется заменить страницу, используется циклический индекс для замены на старую страницу.

Working Set
Описание: Алгоритм Working Set отслеживает набор страниц, которые активно используются в течение определённого времени. 
Цель этого алгоритма — держать в памяти те страницы, которые активно используются, и заменять те, которые не используются.
Применение: В коде таблица Working Set представлена вектором структур WSRow. 
Стратегия замены страниц учитывает флаги чтения и модификации, а также время последнего доступа для определения, какие страницы следует заменить.


Они используются для управления памятью в условиях ограниченных ресурсов, обеспечивая, 
что наиболее актуальные или наиболее часто используемые страницы остаются в памяти, а менее важные страницы заменяются.

В алгоритме FIFO и Working Set используются индексы для доступа к элементам таблиц и управления заменой страниц.

