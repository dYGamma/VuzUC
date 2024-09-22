#include <windows.h>       // Подключение библиотеки для работы с Windows API (потоки, мьютексы, семафоры и т.д.)
#include <iostream>        // Подключение стандартной библиотеки для ввода-вывода
#include "lab3.h"          // Подключение пользовательского заголовочного файла, который может содержать дополнительные функции или определения
using std::cout;           // Использование конкретного элемента из пространства имен std
using std::flush;          // Использование функции для принудительного вывода данных

#define THREADCOUNT 10     // Определение константы для количества потоков

HANDLE mutex;              // Дескриптор мьютекса для синхронизации потоков
HANDLE hThread[THREADCOUNT]; // Массив дескрипторов для каждого потока

/*                      0   1   2   3   4   5   6   7   8   9  */
char charTable[THREADCOUNT] = {'a','b','c','d','e','f','g','h','i','k'}; // Таблица символов, которые выводят потоки

DWORD ThreadID;            // Переменная для хранения идентификатора потока

HANDLE semaphoreTable[10]; // Массив дескрипторов семафоров
/*                          0  1  2  3  4  5  6  7  8  9 */
int semaphoreTableCount[10] = {0, 3, 0, 3, 9, 6, 6, 6, 6, 3}; // Начальные счетчики для семафоров

unsigned int lab3_thread_graph_id()
{
    return 16;  // Возвращает идентификатор графа потоков
}

const char* lab3_unsynchronized_threads()
{
    return "bcef";  // Возвращает символы потоков, которые выполняются без синхронизации
}

const char* lab3_sequential_threads()
{
    return "ehi";   // Возвращает символы потоков, которые выполняются последовательно
}

// Определение прототипов функций потоков
DWORD WINAPI thread_a(LPVOID lpParam);
DWORD WINAPI thread_b(LPVOID lpParam);
DWORD WINAPI thread_c(LPVOID lpParam);
DWORD WINAPI thread_d(LPVOID lpParam);
DWORD WINAPI thread_e(LPVOID lpParam);
DWORD WINAPI thread_f(LPVOID lpParam);
DWORD WINAPI thread_g(LPVOID lpParam);
DWORD WINAPI thread_h(LPVOID lpParam);
DWORD WINAPI thread_i(LPVOID lpParam);
DWORD WINAPI thread_k(LPVOID lpParam);

void thread_unsynchronized(int thread);  // Прототип функции для выполнения несинхронизированных потоков
void thread_sequential(int threads);     // Прототип функции для выполнения последовательных потоков

// Определение функции потока 'a'
DWORD WINAPI thread_a(LPVOID lpParam)
{
    for(int i = 0; i < 3; i++) {
        WaitForSingleObject(mutex, INFINITE);  // Ожидание освобождения мьютекса для синхронизации вывода
        cout << charTable[(int)lpParam] << flush; // Вывод символа, связанного с потоком 'a'
        ReleaseMutex(mutex); // Освобождение мьютекса
        computation();  // Задержка
    }

    // Создание потока 'b'
    hThread[1] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_b, NULL,  0, &ThreadID);
    if( hThread[1] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Создание потока 'c'
    hThread[2] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_c, NULL,  0, &ThreadID);
    if( hThread[2] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Создание потока 'e'
    hThread[4] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_e, NULL,  0, &ThreadID);
    if( hThread[4] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Создание потока 'f'
    hThread[5] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_f, NULL,  0, &ThreadID);
    if( hThread[5] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Ожидание завершения потоков 'b' и 'e'
    WaitForSingleObject(hThread[1], INFINITE);
    WaitForSingleObject(hThread[4], INFINITE);

    ExitThread(0); // Завершение потока 'a'
}

// Определение функции потока 'b'
DWORD WINAPI thread_b(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);  // Параметр lpParam не используется в этой функции

    thread_unsynchronized(1); // Выполнение несинхронизированного кода

    // Ожидание завершения потоков 'c', 'e' и 'f'
    WaitForSingleObject(hThread[2], INFINITE);
    WaitForSingleObject(hThread[4], 1000L);
    WaitForSingleObject(hThread[5], 1000L);

    // Создание потока 'd'
    hThread[3] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_d, NULL,  0, &ThreadID);
    if( hThread[3] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Создание потока 'g'
    hThread[6] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_g, NULL,  0, &ThreadID);
    if( hThread[6] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Освобождение семафора и выполнение последовательного кода
    ReleaseSemaphore(semaphoreTable[1], 1,NULL);
    thread_sequential(13);

    ExitThread(0);  // Завершение потока 'b'
}

// Определение функции потока 'c'
DWORD WINAPI thread_c(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_unsynchronized(2); // Выполнение несинхронизированного кода

    ExitThread(0);  // Завершение потока 'c'
}

// Определение функции потока 'd'
DWORD WINAPI thread_d(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_sequential(34);  // Выполнение последовательного кода

    ExitThread(0);  // Завершение потока 'd'
}

// Определение функции потока 'e'
DWORD WINAPI thread_e(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_unsynchronized(4);  // Выполнение несинхронизированного кода

    WaitForSingleObject(hThread[2], INFINITE); // Ожидание завершения потока 'c'
    thread_sequential(45);  // Выполнение последовательного кода

    // Создание потока 'h'
    hThread[7] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_h, NULL,  0, &ThreadID);
    if( hThread[7] == NULL )
        cout << "CreateThread error: " << GetLastError();

    // Освобождение семафора и выполнение последовательного кода
    ReleaseSemaphore(semaphoreTable[6], 1,NULL);
    thread_sequential(45);

    // Создание потока 'i'
    hThread[8] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_i, NULL,  0, &ThreadID);
    if( hThread[8] == NULL )
        cout << "CreateThread error: " << GetLastError();

    WaitForSingleObject(hThread[5], INFINITE); // Ожидание завершения потока 'f'
    ReleaseSemaphore(semaphoreTable[7], 1,NULL); // Освобождение семафора
    thread_sequential(47);  // Выполнение последовательного кода

    // Ожидание завершения потоков 'h' и 'i'
    WaitForSingleObject(hThread[7], INFINITE);
    WaitForSingleObject(hThread[8], INFINITE);
    ExitThread(0);  // Завершение потока 'e'
}

// Определение функции потока 'f'
DWORD WINAPI thread_f(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_unsynchronized(5);  // Выполнение несинхронизированного кода

    WaitForSingleObject(hThread[2], INFINITE); // Ожидание завершения потока 'c'
    thread_sequential(56);  // Выполнение последовательного кода

    thread_sequential(56);  // Выполнение последовательного кода повторно

    ExitThread(0);  // Завершение потока 'f'
}

// Определение функции потока 'g'
DWORD WINAPI thread_g(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    WaitForSingleObject(hThread[2], INFINITE); // Ожидание завершения потока 'c'
    thread_sequential(61);  // Выполнение последовательного кода

    thread_sequential(67);  // Выполнение последовательного кода повторно

    ExitThread(0);  // Завершение потока 'g'
}

// Определение функции потока 'h'
DWORD WINAPI thread_h(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_sequential(74);  // Выполнение последовательного кода

    thread_sequential(78);  // Выполнение последовательного кода повторно
    ExitThread(0);  // Завершение потока 'h'
}

// Определение функции потока 'i'
DWORD WINAPI thread_i(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_sequential(84);  // Выполнение последовательного кода

    // Создание потока 'k'
    hThread[9] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_k, NULL,  0, &ThreadID);
    if( hThread[9] == NULL )
        cout << "CreateThread error: " << GetLastError();

    ReleaseSemaphore(semaphoreTable[9], 1,NULL); // Освобождение семафора
    thread_sequential(89);  // Выполнение последовательного кода

    WaitForSingleObject(hThread[9], INFINITE); // Ожидание завершения потока 'k'
    ExitThread(0);  // Завершение потока 'i'
}

// Определение функции потока 'k'
DWORD WINAPI thread_k(LPVOID lpParam)
{
    UNREFERENCED_PARAMETER(lpParam);

    thread_sequential(98);  // Выполнение последовательного кода

    ExitThread(0);  // Завершение потока 'k'
}

// Функция для выполнения несинхронизированных потоков
void thread_unsynchronized(int thread)
{
    for(int i = 0; i < 3; i++) {
        WaitForSingleObject(mutex, INFINITE); // Ожидание освобождения мьютекса
        cout << charTable[thread] << flush; // Вывод символа, связанного с потоком
        ReleaseMutex(mutex); // Освобождение мьютекса
        computation();  // Задержка
    }
}

// Функция для выполнения последовательных потоков
void thread_sequential(int threads)
{
    DWORD dwWaitResult;
    BOOL bContinue;
    for(int i = 0; i < 3; i++)
    {
        bContinue=TRUE;
        while(bContinue)
        {
            dwWaitResult = WaitForSingleObject(semaphoreTable[(int)threads/10],60000L); // Ожидание освобождения семафора
            switch (dwWaitResult)
            {
                case WAIT_OBJECT_0:
                    WaitForSingleObject(mutex, INFINITE); // Ожидание освобождения мьютекса
                    cout << charTable[(int)threads/10] << flush; // Вывод символа, связанного с потоком
                    ReleaseMutex(mutex); // Освобождение мьютекса
                    computation();  // Задержка

                    bContinue=FALSE;
                    if(!ReleaseSemaphore(semaphoreTable[(int)threads%10], 1,NULL)) // Освобождение следующего семафора
                    {
                        cout << "ReleaseSemaphore error: " << GetLastError();
                    }
                    break;
                case WAIT_TIMEOUT:
                    cout << "Thread %d: wait timed out\n" << GetCurrentThreadId(); // Вывод ошибки в случае тайм-аута ожидания
                    break;
            }
        }
    }
}

// Функция инициализации потоков и синхронизации
int lab3_init()
{
    mutex = CreateMutex(NULL, FALSE, NULL); // Создание мьютекса

    if(mutex == NULL)
    {
        cout << "CreateMutex error: " << GetLastError(); // Вывод ошибки, если мьютекс не удалось создать
        return 1;
    }

    for(int i = 0; i < 10; i++)
    {
        if(i != 0 && i != 2)
        {
            semaphoreTable[i] = CreateSemaphore(NULL, 0, semaphoreTableCount[i], NULL); // Создание семафоров для потоков, кроме 0 и 2
            if (semaphoreTable[i] == NULL)
            {
                cout << "CreateSemaphore " << i << " error : " <<  GetLastError(); // Вывод ошибки, если семафор не удалось создать
                return 1;
            }
        }
    }

    // Создание потока 'a'
    hThread[0] = CreateThread(NULL,0, (LPTHREAD_START_ROUTINE) thread_a, 0,  0, &ThreadID);
    if( hThread[0] == NULL )
        cout << "CreateThread error: " << GetLastError(); // Вывод ошибки, если поток не удалось создать

    WaitForSingleObject(hThread[0], INFINITE); // Ожидание завершения потока 'a'

    for(int i = 0; i < THREADCOUNT; i++)
        CloseHandle(hThread[i]); // Закрытие всех дескрипторов потоков

    for(int i = 0; i < 10; i++)
    {
        if(i != 0 && i != 2)
            CloseHandle(semaphoreTable[i]); // Закрытие всех дескрипторов семафоров
    }

    CloseHandle(mutex); // Закрытие мьютекса

    return 0; // Завершение функции инициализации
}



Код использует функции Windows API для работы с потоками, мьютексами и семафорами. 
HANDLE — это дескриптор объекта, который используется для управления ресурсами, такими как потоки, мьютексы и семафоры.

Мьютекс (mutex) используется для обеспечения эксклюзивного доступа к разделяемым ресурсам (например, к выводу символов в консоль). 
Семафоры (semaphoreTable) обеспечивают синхронизацию выполнения потоков, позволяя контролировать порядок их выполнения.

Код запускает несколько потоков, каждый из которых выполняет определенную работу, такую как вывод символов. Потоки создаются с помощью функции CreateThread, 
которая принимает указатель на функцию потока (LPTHREAD_START_ROUTINE), параметры для потока, 
флаги и указатель на переменную для идентификатора потока.

Важно, чтобы потоки выполнялись в определенном порядке. 
Это достигается с помощью мьютексов и семафоров. Например, потоки 'b', 'c', 'e' и 'f' запускаются после завершения потока 'a', 
и их выполнение контролируется с помощью WaitForSingleObject.

Функция WaitForSingleObject — это одна из важнейших функций Windows API, используемая для синхронизации потоков. 
Она позволяет потоку ожидать выполнения определённого события или освобождения ресурса (мьютекса, семафора, события и т.д.).

hHandle: Это дескриптор объекта синхронизации, который может быть мьютексом, семафором, событием или другим объектом. 
Программа будет ожидать, пока этот объект не станет "доступным"