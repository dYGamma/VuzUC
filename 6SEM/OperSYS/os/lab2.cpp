#include "lab2.h"             // Подключаем заголовочный файл, содержащий объявления функций и переменных, используемых в этом коде.
#include <cstring>            // Подключаем библиотеку для работы с C-строками, т.е., функциями для работы с массивами символов.
#include <semaphore.h>        // Подключаем библиотеку для работы с семафорами, которые будут использоваться для синхронизации потоков.

// Объявляем глобальный мьютекс, который будет использоваться для защиты критических секций кода.
pthread_mutex_t mutex;

// Объявляем несколько семафоров, которые будут использоваться для синхронизации различных потоков.
sem_t threadSemSyncM, threadSemSyncK, threadSemSyncG, threadSemSyncN;
sem_t threadSemB, threadSemC, threadSemF, threadSemD, threadSemE, threadSemI,
    threadSemM, threadSemN, threadSemR, threadSemH, threadSemP, threadSemG;

// Функция, возвращающая идентификатор графа выполнения потоков.
unsigned int lab2_t}

// Функция, возвращающая строку с именами потоков, которые не должны быть синхронизированы.
const char* lab2_unsynchronized_threads() {
    return "bcf";  // Возвращаем строку с именами потоков 'b', 'c' и 'f'.
}

// Функция, возвращающая строку с именами потоков, которые должны выполняться последовательно.
const char* lab2_sequential_threads() {
    return "gkmn";  // Возвращаем строку с именами потоков 'g', 'k', 'm' и 'n'.
}

// Функция для создания и запуска потока.
pthread_t executeJob(void *(*jobFunc)(void *)) {
    pthread_t jobId;                          // Объявляем переменную для идентификатора потока.
    pthread_create(&jobId, NULL, jobFunc, NULL);  // Создаем новый поток, который будет выполнять функцию jobFunc.
    return jobId;                             // Возвращаем идентификатор созданного потока.
}

// Функция, которая выводит строку данных с использованием мьютекса для защиты от одновременного доступа.
void printWithMutex(const std::string &data) {
    for (int i = 0; i < 3; ++i) {               // Выполняем цикл 3 раза.
        pthread_mutex_lock(&mutex);             // Блокируем мьютекс перед выводом данных.
        std::cout << data << std::flush;        // Выводим данные и принудительно очищаем буфер.
        pthread_mutex_unlock(&mutex);           // Разблокируем мьютекс после вывода.
        computation();                          // искусственная задержка (для выполнения задачи)
    }
}

// Функция для синхронизированного вывода данных с использованием семафоров.
void printSem(const std::string &data, sem_t &actualSem, sem_t &actualFollowing) {
    for (int i = 0; i < 3; ++i) {               // Выполняем цикл 3 раза.
        sem_wait(&actualSem);                   // Ожидаем сигнала на семафоре actualSem перед началом вывода.
        std::cout << data << std::flush;        // Выводим данные и принудительно очищаем буфер.
        sem_post(&actualFollowing);             // Отправляем сигнал на семафоре actualFollowing после завершения вывода.
        computation();                          // искусственная задержка (для выполнения задачи)
    }
}

// Объявление функций потоков (их определения находятся позже в коде).
void *jobF(void *p);
void *jobA(void *p) {
    printWithMutex("a");                          // Выводим "a" с использованием мьютекса.
    pthread_join(executeJob(jobF), NULL);         // Запускаем поток F и ожидаем его завершения.
    return p;                                     // Возвращаем указатель на входные данные (в данном случае просто NULL).
}

void *jobG(void *p);
void *jobB(void *p) {
    printWithMutex("b");                          // Выводим "b" с использованием мьютекса.

    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.
    sem_wait(&threadSemB);                        // Ожидаем сигнал на семафоре B (от потока F).
    sem_wait(&threadSemB);                        // Ожидаем сигнал на семафоре B (от потока C).

    executeJob(jobG);                             // Запускаем поток G.
    return p;
}

void *jobH(void *p);
void *jobC(void *p) {
    printWithMutex("c");                          // Выводим "c" с использованием мьютекса.

    sem_post(&threadSemB);                        // Отправляем сигнал на семафоре B.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока F).
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока B).

    printWithMutex("c");                          // Снова выводим "c" с использованием мьютекса.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.
    sem_post(&threadSemD);                        // Отправляем сигнал на семафоре D.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока G).
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока E).
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока D).
    sem_wait(&threadSemC);                        // Ожидаем сигнал на семафоре C (от потока F).
    executeJob(jobH);                             // Запускаем поток H.
    return p;
}

void *jobD(void *p) {
    printWithMutex("d");                          // Выводим "d" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.
    return p;
}

void *jobE(void *p) {
    printWithMutex("e");                          // Выводим "e" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemD);                        // Отправляем сигнал на семафоре D.
    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.

    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока G).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока D).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока C).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока F).

    printWithMutex("e");                          // Снова выводим "e" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemH);                        // Отправляем сигнал на семафоре H.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.

    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока G).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока R).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока H).
    sem_wait(&threadSemE);                        // Ожидаем сигнал на семафоре E (от потока F).

    printWithMutex("e");                          // Еще раз выводим "e" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemI);                        // Отправляем сигнал на семафоре I.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.
    return p;
}

void *jobG(void *p) {
    executeJob(jobE);                             // Запускаем поток E.
    executeJob(jobD);                             // Запускаем поток D.

    printWithMutex("g");                          // Выводим "g" с использованием мьютекса.

    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemD);                        // Отправляем сигнал на семафоре D.
    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.

    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока E).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока D).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока C).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока F).

    printWithMutex("g");                          // Снова выводим "g" с использованием мьютекса.

    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemH);                        // Отправляем сигнал на семафоре H.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.

    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока E).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока R).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока H).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока F).

    printWithMutex("g");                          // Еще раз выводим "g" с использованием мьютекса.

    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemI);                        // Отправляем сигнал на семафоре I.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.

    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока E).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока R).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока I).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока M).
    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G (от потока N).

    printSem("g", threadSemSyncG, threadSemSyncK);  // Синхронизированный вывод "g" с помощью семафоров.

    sem_wait(&threadSemG);                        // Ожидаем сигнал на семафоре G.

    printWithMutex("g");                          // Еще раз выводим "g" с использованием мьютекса.

    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.
    return p;
}

void *jobN(void *p);
void *jobF(void *p) {
    executeJob(jobB);                             // Запускаем поток B.
    executeJob(jobC);                             // Запускаем поток C.

    printWithMutex("f");                          // Выводим "f" с использованием мьютекса.

    sem_post(&threadSemB);                        // Отправляем сигнал на семафоре B.
    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока C).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока B).

    printWithMutex("f");                          // Снова выводим "f" с использованием мьютекса.

    sem_post(&threadSemC);                        // Отправляем сигнал на семафоре C.
    sem_post(&threadSemD);                        // Отправляем сигнал на семафоре D.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.

    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока G).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока E).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока D).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока C).

    printWithMutex("f");                          // Еще раз выводим "f" с использованием мьютекса.

    sem_post(&threadSemH);                        // Отправляем сигнал на семафоре H.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.

    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока G).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока E).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока R).
    sem_wait(&threadSemF);                        // Ожидаем сигнал на семафоре F (от потока H).

    pthread_join(executeJob(jobN), NULL);         // Запускаем поток N и ожидаем его завершения.
    return p;
}

void *jobK(void *p) {
    printSem("k", threadSemSyncK, threadSemSyncM);  // Синхронизированный вывод "k" с помощью семафоров.
    return p;
}

void *jobI(void *p) {
    printWithMutex("i");                          // Выводим "i" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.

    sem_wait(&threadSemI);                        // Ожидаем сигнал на семафоре I (от потока G).
    sem_wait(&threadSemI);                        // Ожидаем сигнал на семафоре I (от потока E).
    sem_wait(&threadSemI);                        // Ожидаем сигнал на семафоре I (от потока R).
    sem_wait(&threadSemI);                        // Ожидаем сигнал на семафоре I (от потока M).
    sem_wait(&threadSemI);                        // Ожидаем сигнал на семафоре I (от потока N).

    executeJob(jobK);                             // Запускаем поток K.
    return p;
}

void *jobR(void *p) {
    printWithMutex("r");                          // Выводим "r" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.

    sem_wait(&threadSemR);                        // Ожидаем сигнал на семафоре R (от потока G).
    sem_wait(&threadSemR);                        // Ожидаем сигнал на семафоре R (от потока E).
    sem_wait(&threadSemR);                        // Ожидаем сигнал на семафоре R (от потока H).
    sem_wait(&threadSemR);                        // Ожидаем сигнал на семафоре R (от потока F).

    printWithMutex("r");                          // Снова выводим "r" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemI);                        // Отправляем сигнал на семафоре I.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.

    return p;
}


void *jobH(void *p) {
    executeJob(jobR);                             // Запускаем поток R.

    printWithMutex("h");                          // Выводим "h" с использованием мьютекса.
    sem_post(&threadSemF);                        // Отправляем сигнал на семафоре F.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    return p;
}

void *jobP(void *p);
void *jobM(void *p) {
    printWithMutex("m");                          // Выводим "m" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemE);                        // Отправляем сигнал на семафоре E.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.
    sem_post(&threadSemI);                        // Отправляем сигнал на семафоре I.

    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока G).
    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока E).
    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока R).
    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока I).
    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока N).

    printSem("m", threadSemSyncM, threadSemSyncN);  // Синхронизированный вывод "m" с помощью семафоров.
    sem_wait(&threadSemM);                        // Ожидаем сигнал на семафоре M (от потока N).
    executeJob(jobP);                             // Запускаем поток P.
    return p;
}

void *jobN(void *p) {
    executeJob(jobI);                             // Запускаем поток I.
    executeJob(jobM);                             // Запускаем поток M.

    printWithMutex("n");                          // Выводим "n" с использованием мьютекса.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemR);                        // Отправляем сигнал на семафоре R.
    sem_post(&threadSemI);                        // Отправляем сигнал на семафоре I.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока M).
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока I).
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока R).
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока E).
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока G).

    printSem("n", threadSemSyncN, threadSemSyncG);  // Синхронизированный вывод "n" с помощью семафоров.

    sem_post(&threadSemG);                        // Отправляем сигнал на семафоре G.
    sem_post(&threadSemM);                        // Отправляем сигнал на семафоре M.

    printWithMutex("n");                          // Еще раз выводим "n" с использованием мьютекса.

    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока P).
    sem_wait(&threadSemN);                        // Ожидаем сигнал на семафоре N (от потока G).
    return p;
}

void *jobP(void *p) {
    printWithMutex("p");                          // Выводим "p" с использованием мьютекса.
    sem_post(&threadSemN);                        // Отправляем сигнал на семафоре N.
    return p;
}

int lab2_init() {
    // Инициализация мьютекса
    pthread_mutex_init(&mutex, NULL);

    // Инициализация всех семафоров
    sem_init(&threadSemB, 0, 0);
    sem_init(&threadSemC, 0, 0);
    sem_init(&threadSemD, 0, 0);
    sem_init(&threadSemE, 0, 0);
    sem_init(&threadSemF, 0, 0);
    sem_init(&threadSemI, 0, 0);
    sem_init(&threadSemN, 0, 0);
    sem_init(&threadSemH, 0, 0);
    sem_init(&threadSemG, 0, 0);
    sem_init(&threadSemP, 0, 0);
    sem_init(&threadSemR, 0, 0);
    sem_init(&threadSemSyncM, 0, 0);
    sem_init(&threadSemSyncK, 0, 0);
    sem_init(&threadSemSyncG, 0, 1);              // Семафор G начинается с 1, т.к. G первый в последовательности.
    sem_init(&threadSemSyncN, 0, 0);

    // Запуск основного потока A и ожидание его завершения
    pthread_join(executeJob(jobA), NULL);

    // Уничтожение мьютекса и семафоров после завершения работы всех потоков
    pthread_mutex_destroy(&mutex);
    sem_destroy(&threadSemB);
    sem_destroy(&threadSemC);
    sem_destroy(&threadSemD);
    sem_destroy(&threadSemE);
    sem_destroy(&threadSemF);
    sem_destroy(&threadSemI);
    sem_destroy(&threadSemN);
    sem_destroy(&threadSemH);
    sem_destroy(&threadSemG);
    sem_destroy(&threadSemP);
    sem_destroy(&threadSemR);
    sem_destroy(&threadSemSyncM);
    sem_destroy(&threadSemSyncK);
    sem_destroy(&threadSemSyncG);
    sem_destroy(&threadSemSyncN);

    return 0;
}



В представленной программе используются потоки, которые взаимодействуют между собой посредством семафоров и мьютекса.

Семафоры используются для синхронизации выполнения потоков, обеспечивая строгий порядок их чередования. 
Каждый поток выполняется только после того, как получает соответствующий сигнал (освобождение семафора) от другого потока. 
Это создаёт строгое чередование, то есть поток не начнёт выполнение до тех пор, пока предыдущий поток не завершится и не освободит семафор.

Захват семафора (sem_wait) означает, что поток ждёт освобождения семафора другим потоком. Как только семафор освобождается (количество ресурсов в семафоре увеличивается), 
поток продолжает своё выполнение.
Освобождение семафора (sem_post) сигнализирует другим потокам, что текущий поток завершил свою критическую секцию, и они могут продолжать выполнение.
В коде видно, что один поток освобождает семафор для другого потока, позволяя ему продолжать работу. 
Например, поток A после выполнения своей задачи вызывает sem_post(&threadSemB), что позволяет потоку B начать свою работу.

Мьютексы используются для защиты критических секций кода, которые могут быть выполнены одновременно несколькими потоками. 
Это предотвращает ситуации гонок, когда несколько потоков пытаются одновременно модифицировать общие данные.

Захват мьютекса (pthread_mutex_lock) означает, что поток захватывает мьютекс, и другие потоки не могут войти в защищённую секцию, пока мьютекс не будет освобождён.
Освобождение мьютекса (pthread_mutex_unlock) освобождает мьютекс, позволяя другим потокам войти в защищённую секцию.
В коде мьютекс используется для синхронизации вывода символов на экран (например, printWithMutex("a")), 
чтобы избежать одновременного вывода символов несколькими потоками, что может привести к искажению результата.

Строгое чередование
Строгое чередование в данной программе достигается через последовательное захватывание и освобождение семафоров. 
Каждый поток ожидает освобождения определённого семафора перед началом работы и освобождает другой семафор после завершения своей работы. 
Это гарантирует, что потоки выполняются в строго определённом порядке.

Предположим, у нас есть два потока: A и B. Поток A завершает свою работу и вызывает sem_post(&threadSemB), что сигнализирует потоку B начать выполнение. 
Поток B, в свою очередь, ждёт, пока поток A выполнит свою работу (через sem_wait(&threadSemB)), 
и только после этого начинает свою работу.