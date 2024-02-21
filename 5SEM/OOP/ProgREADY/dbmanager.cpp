
#include "dbmanager.h"
#include "dbnames.h"

DbManager::DbManager()
    : Singleton<DbManager>(*this) {
}

void DbManager::connectToDB() {
    if(!QFile(DATABASE_NAME).exists()){
        this->restoreDataBase();
    } else {
        this->openDataBase();
    }
}

bool DbManager::restoreDataBase() {
    if(this->openDataBase()){
        if(!this->createVehiclesTable() ||
            !this->createCustomersTable() ||
            !this->createManufacturersTable() ||
            !this->createDealerShipsTable() ||
            !this->createSalesTable()){
            return false;
        } else {
            return true;
        }
    } else {
        qDebug() << "Не удалось восстановить базу данных";
        return false;
    }
    return false;
}

bool DbManager::openDataBase() {
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(DATABASE_NAME);
    if(db.open()){
        return true;
    } else {
        return false;
    }
}

void DbManager::closeDataBase() {
    db.close();
}

bool DbManager::createVehiclesTable(){
    QSqlQuery query;
    if(!query.exec( "CREATE TABLE " VEHICLES_TABLE " ("
                    VEHICLE_ID " INTEGER PRIMARY KEY AUTOINCREMENT, "
                    VEHICLE_MARK        " VARCHAR(255)     NOT NULL,"
                    VEHICLE_MODEL       " VARCHAR(255)     NOT NULL,"
                    VEHICLE_YEAR        " INTEGER          NOT NULL,"
                    VEHICLE_PRICE       " INTEGER          NOT NULL,"
                    VEHICLE_DESCRIPTION " VARCHAR(255)     NOT NULL,"
                    VEHICLE_STATUS      " VARCHAR(255)     NOT NULL"
                    " )"
                    )){
        qDebug() << "DataBase: error of create " << VEHICLES_TABLE;
        qDebug() << query.lastError().text();
        return false;
    } else {
        return true;
    }
    return false;
}
bool DbManager::createManufacturersTable(){
    QSqlQuery query;
    if(!query.exec( "CREATE TABLE " MANUFACTURERS_TABLE " ("
                    MANUFACTURER_ID " INTEGER PRIMARY KEY AUTOINCREMENT, "
                    MANUFACTURER_NAME       " VARCHAR(255)     NOT NULL,"
                    MANUFACTURER_COUNTRY    " VARCHAR(255)     NOT NULL"
                    " )"
                    )){
        qDebug() << "DataBase: error of create " << MANUFACTURERS_TABLE;
        qDebug() << query.lastError().text();
        return false;
    } else {
        return true;
    }
    return false;
}
bool DbManager::createDealerShipsTable(){
    QSqlQuery query;
    if(!query.exec( "CREATE TABLE " DEALERSHIPS_TABLE " ("
                    DEALERSHIP_ID " INTEGER PRIMARY KEY AUTOINCREMENT, "
                    DEALERSHIP_NAME     " VARCHAR(255)     NOT NULL,"
                    DEALERSHIP_ADDRESS  " VARCHAR(255)     NOT NULL"
                    " )"
                    )){
        qDebug() << "DataBase: error of create " << DEALERSHIPS_TABLE;
        qDebug() << query.lastError().text();
        return false;
    } else {
        return true;
    }
    return false;
}

bool DbManager::createCustomersTable() {
    QSqlQuery query;
    if(!query.exec( "CREATE TABLE " CUSTOMERS_TABLE " ("
                    CUSTOMER_ID " INTEGER PRIMARY KEY AUTOINCREMENT, "
                    CUSTOMER_FNAME      " VARCHAR(255)    NOT NULL,"
                    CUSTOMER_LNAME      " VARCHAR(255)    NOT NULL,"
                    CUSTOMER_CONTACTS   " VARCHAR(255)    NOT NULL"
                    " )"
                    )){
        qDebug() << "DataBase: error of create " << CUSTOMERS_TABLE;
        qDebug() << query.lastError().text();
        return false;
    } else {
        return true;
    }
    return false;
}

bool DbManager::createSalesTable(){
    QSqlQuery query;
    if(!query.exec( "CREATE TABLE " SALES_TABLE " ("
                    SALE_ID " INTEGER PRIMARY KEY AUTOINCREMENT, "
                    SALE_DATE       " TEXT             NOT NULL,"
                    SALE_DEALER     " VARCHAR(255)     NOT NULL,"
                    SALE_CUSTOMER   " INTEGER          NOT NULL,"
                    SALE_VEHICLE    " INTEGER          NOT NULL,"
                    SALE_AMOUNT     " VARCHAR(255)     NOT NULL,"
                    "FOREIGN KEY (" SALE_CUSTOMER ") REFERENCES " CUSTOMERS_TABLE " (" CUSTOMER_ID "),"
                    "FOREIGN KEY (" SALE_AMOUNT ") REFERENCES " VEHICLES_TABLE " (" VEHICLE_ID ")"
                    " );"
                    )){
        qDebug() << "DataBase: error of create " << SALES_TABLE;
        qDebug() << query.lastError().text();
        return false;
    } else {
        return true;
    }
    return false;
}


QVector<Vehicle> DbManager::getVehicles() {
    QVector<Vehicle> result;
    QSqlQuery query;
    if(!query.exec("SELECT * FROM " VEHICLES_TABLE)){
        qDebug() << "DataBase: error of select " << VEHICLES_TABLE;
        return result;
    }
    QSqlRecord rec = query.record();
    while (query.next()) {
        Vehicle v;
        v.id = query.value(rec.indexOf(VEHICLE_ID)).toInt();
        v.mark = query.value(rec.indexOf(VEHICLE_MARK)).toString();
        v.model = query.value(rec.indexOf(VEHICLE_MODEL)).toString();
        v.year = query.value(rec.indexOf(VEHICLE_YEAR)).toInt();
        v.price = query.value(rec.indexOf(VEHICLE_PRICE)).toInt();
        v.description = query.value(rec.indexOf(VEHICLE_DESCRIPTION)).toString();
        v.status = query.value(rec.indexOf(VEHICLE_STATUS)).toString();

        result.append(v);
    }

    return result;
}

bool DbManager::insertVehicle(Vehicle* v) {
    QString query_string = "INSERT INTO " VEHICLES_TABLE "("
                            VEHICLE_MARK       ", "
                            VEHICLE_MODEL      ", "
                            VEHICLE_YEAR       ", "
                            VEHICLE_PRICE      ", "
                            VEHICLE_DESCRIPTION", "
                            VEHICLE_STATUS ") "
                           "VALUES ('%1', '%2', %3, %4, '%5', '%6');";
    query_string = query_string.arg(v->mark)
        .arg(v->model)
        .arg(v->year)
        .arg(v->price)
        .arg(v->description)
        .arg(v->status);

    QSqlQuery query;
    if(!query.exec(query_string)){
        qDebug() << "DataBase: error of insert " << VEHICLES_TABLE;
        return false;
    }

    return true;
}

QVector<Manufacturer> DbManager::getManufacturers() {
    QVector<Manufacturer> result;
    QSqlQuery query;
    if(!query.exec("SELECT * FROM " MANUFACTURERS_TABLE)){
        qDebug() << "DataBase: error of select " << MANUFACTURERS_TABLE;
        return result;
    }
    QSqlRecord rec = query.record();
    while (query.next()) {
        Manufacturer m;
        m.id = query.value(rec.indexOf(MANUFACTURER_ID)).toInt();
        m.name = query.value(rec.indexOf(MANUFACTURER_NAME)).toString();
        m.country = query.value(rec.indexOf(MANUFACTURER_COUNTRY)).toString();

        result.append(m);
    }

    return result;
}

bool DbManager::insertManufacturer(Manufacturer* m) {
    QString query_string = "INSERT INTO " MANUFACTURERS_TABLE "("
                            MANUFACTURER_NAME       ", "
                            MANUFACTURER_COUNTRY    ") "
                           "VALUES ('%1', '%2');";
    query_string = query_string
                       .arg(m->name)
                       .arg(m->country);

    QSqlQuery query;
    if(!query.exec(query_string)){
        qDebug() << "DataBase: error of insert " << MANUFACTURERS_TABLE;
        return false;
    }

    return true;
}

QVector<Customer> DbManager::getCustomers() {
    QVector<Customer> result;
    QSqlQuery query;
    if(!query.exec("SELECT * FROM " CUSTOMERS_TABLE)){
        qDebug() << "DataBase: error of select " << CUSTOMERS_TABLE;
        return result;
    }
    QSqlRecord rec = query.record();
    while (query.next()) {
        Customer c;
        c.id = query.value(rec.indexOf(CUSTOMER_ID)).toInt();
        c.first_name = query.value(rec.indexOf(CUSTOMER_FNAME)).toString();
        c.last_name = query.value(rec.indexOf(CUSTOMER_LNAME)).toString();
        c.contacts = query.value(rec.indexOf(CUSTOMER_CONTACTS)).toString();

        result.append(c);
    }

    return result;
}

bool DbManager::insertCustomer(Customer* c) {
    QString query_string = "INSERT INTO " CUSTOMERS_TABLE "("
                            CUSTOMER_FNAME       ", "
                            CUSTOMER_LNAME       ", "
                            CUSTOMER_CONTACTS    ") "
                           "VALUES ('%1', '%2', '%3');";
    query_string = query_string
                       .arg(c->first_name)
                       .arg(c->last_name)
                       .arg(c->contacts);

    QSqlQuery query;
    if(!query.exec(query_string)){
        qDebug() << "DataBase: error of insert " << CUSTOMERS_TABLE;
        return false;
    }

    return true;
}

QVector<Dealership> DbManager::getDealerships() {
    QVector<Dealership> result;
    QSqlQuery query;
    if(!query.exec("SELECT * FROM " DEALERSHIPS_TABLE)){
        qDebug() << "DataBase: error of select " << DEALERSHIPS_TABLE;
        return result;
    }
    QSqlRecord rec = query.record();
    while (query.next()) {
        Dealership d;
        d.id = query.value(rec.indexOf(DEALERSHIP_ID)).toInt();
        d.name = query.value(rec.indexOf(DEALERSHIP_NAME)).toString();
        d.address = query.value(rec.indexOf(DEALERSHIP_ADDRESS)).toString();

        result.append(d);
    }

    return result;
}

bool DbManager::insertDealership(Dealership* d) {
    QString query_string = "INSERT INTO " DEALERSHIPS_TABLE "("
                            DEALERSHIP_NAME       ", "
                            DEALERSHIP_ADDRESS    ") "
                           "VALUES ('%1', '%2');";
    query_string = query_string
                       .arg(d->name)
                       .arg(d->address);

    QSqlQuery query;
    if(!query.exec(query_string)){
        qDebug() << "DataBase: error of insert " << DEALERSHIPS_TABLE;
        return false;
    }

    return true;
}

QSqlQuery DbManager::getSales() {
    QString query_string = "SELECT t1." SALE_ID
                           ", t1." SALE_DATE
                           ", t1." SALE_DEALER
                           ", t2." CUSTOMER_LNAME
                           ", t3." VEHICLE_MARK
                           ", t1." SALE_AMOUNT
                           " FROM " SALES_TABLE " t1 "
                           "JOIN " CUSTOMERS_TABLE " t2 ON t1." SALE_CUSTOMER "=t2." CUSTOMER_ID " "
                           "JOIN " VEHICLES_TABLE " t3 ON t1." SALE_VEHICLE "=t3." VEHICLE_ID ";";
    QSqlQuery query;
    query.exec(query_string);
    return query;
}

bool DbManager::insertSale(Sale* s) {
    QString query_string = "INSERT INTO " SALES_TABLE "("
                            SALE_DATE      ", "
                            SALE_DEALER    ", "
                            SALE_CUSTOMER  ", "
                            SALE_VEHICLE   ", "
                            SALE_AMOUNT    ") "
                           "VALUES ('%1', '%2', '%3', '%4', %5);";
    query_string = query_string
                       .arg(s->date.toString())
                       .arg(s->dealer)
                       .arg(s->customer)
                       .arg(s->vehicle)
                       .arg(s->amount);

    QSqlQuery query;
    if(!query.exec(query_string)){
        qDebug() << "DataBase: error of insert " << SALES_TABLE;
        return false;
    }

    return true;
}

