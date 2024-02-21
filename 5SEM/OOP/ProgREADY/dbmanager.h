
#ifndef DBMANAGER_H
#define DBMANAGER_H

#include <QObject>
#include <QSql>
#include <QSqlQuery>
#include <QSqlError>
#include <QSqlDatabase>
#include <QFile>
#include <QDate>
#include <QDebug>
#include <QVector>
#include <QSqlRecord>

#include "model.h"

// шаблон для реализации паттерна синглтон
template <class T>
class Singleton {
public:
    // конструктор
    Singleton(T& rObject) {
        Q_ASSERT_X(!s_pInstance, "constructor", "Only one instance of this class is permitted.");
        s_pInstance = &rObject;
    }
    // деструктор
    ~Singleton() {
        Q_ASSERT_X(s_pInstance, "destructor", "The singleton instance is invalid.");
        s_pInstance = 0;
    }
    // получение ссылки на объект
    static T& instance() {
        if(!s_pInstance) {
            s_pInstance = new T();
        }

        return (*s_pInstance);
    }
private:
    // указатель на объект
    static T* s_pInstance;
    // приватный конструктор
    Singleton(const Singleton& Src);
    // перегрузка оператора =
    Singleton& operator=(const Singleton& Src);
};
template <class T> T* Singleton<T>::s_pInstance = 0;

class   DbManager;
#define example DbManager::instance()

// класс для взаимодействия с БД
class DbManager : public Singleton<DbManager> {
public:
    // конструктор
    DbManager();

    // метод подключения к БД
    void connectToDB();

    // получение всех транспортных средств
    QVector<Vehicle> getVehicles();
    // добавление тр. средства
    bool insertVehicle(Vehicle* v);

    // получение всех производителей
    QVector<Manufacturer> getManufacturers();
    // добавление производителя
    bool insertManufacturer(Manufacturer* m);

    // получение всех покупателей
    QVector<Customer> getCustomers();
    // добавление покупателя
    bool insertCustomer(Customer* c);

    // получение всех дилерских центров
    QVector<Dealership> getDealerships();
    // добавление центра
    bool insertDealership(Dealership* d);

    // получение всех продаж
    QSqlQuery getSales();
    // добавление продажи
    bool insertSale(Sale* s);

private:
    // БД
    QSqlDatabase    db;

    // открытие БД
    bool openDataBase();
    // восстановление БД
    bool restoreDataBase();
    // закрытие БД
    void closeDataBase();
    // методы создания таблиц в БД
    bool createVehiclesTable();
    bool createManufacturersTable();
    bool createDealerShipsTable();
    bool createCustomersTable();
    bool createSalesTable();

};

#endif // DBMANAGER_H
