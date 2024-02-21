
#ifndef MODEL_H
#define MODEL_H

#include <QString>
#include <QDate>

// классы модели

class Vehicle {
public:
    int id;
    QString mark;
    QString model;
    int year;
    int price;
    QString description;
    QString status;
};

class Manufacturer{
public:
    int id;
    QString name;
    QString country;
};

class Dealership {
public:
    int id;
    QString name;
    QString address;
};

class Customer {
public:
    int id;
    QString first_name;
    QString last_name;
    QString contacts;
};

class Sale {
public:
    int id;
    QDate date;
    QString dealer;
    int customer;
    int vehicle;
    int amount;
};

#endif // MODEL_H
