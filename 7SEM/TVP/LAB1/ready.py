# Итеративная версия функции 5x + y
def iterative_function(x, y):
    """
    Вычисляет 5x + y итеративным способом.
    """
    result = 0
    for _ in range(5):  # 5 раз добавляем x
        result += x
    result += y  # Добавляем y
    return result

# Рекурсивная версия функции 5x + y
def recursive_function(x, y, multiplier=5):
    """
    Вычисляет 5x + y рекурсивным способом.
    """
    if multiplier == 0:
        return y  # Когда множитель равен 0, добавляем y
    return x + recursive_function(x, y, multiplier - 1)

# Функции для безопасного ввода значений
def input_integer(prompt):
    """
    Запрашивает ввод целого числа у пользователя.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: пожалуйста, введите корректное целое число.")

# Главная программа
def main():
    """
    Главная функция программы. Сравнивает итеративный и рекурсивный способы вычисления.
    """
    # Ввод значений x и y
    x = input_integer("Введите значение x: ")
    y = input_integer("Введите значение y: ")

    # Вычисление итеративным способом
    result_iterative = iterative_function(x, y)
    print(f"Итеративный результат: {result_iterative}")

    # Вычисление рекурсивным способом
    result_recursive = recursive_function(x, y)
    print(f"Рекурсивный результат: {result_recursive}")

    # Проверка совпадения результатов
    if result_iterative == result_recursive:
        print("Результаты совпадают!")
    else:
        print("Ошибка: результаты не совпадают.")

# Запуск программы
if __name__ == "__main__":
    main()
