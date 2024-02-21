
#ifndef DBNAMES_H
#define DBNAMES_H

// имя файла БД
#define DATABASE_NAME       "DataBase.db"

// имена таблиц БД
#define VEHICLES_TABLE       "Vehicles"
#define MANUFACTURERS_TABLE  "Manufacturers"
#define DEALERSHIPS_TABLE    "DealerShips"
#define CUSTOMERS_TABLE      "Customers"
#define SALES_TABLE          "Sales"

// имена полей в таблицах БД
#define VEHICLE_ID           "Id"
#define VEHICLE_MARK         "Mark"
#define VEHICLE_MODEL        "Model"
#define VEHICLE_YEAR         "Year"
#define VEHICLE_PRICE        "Price"
#define VEHICLE_DESCRIPTION  "Description"
#define VEHICLE_STATUS       "Status"

#define MANUFACTURER_ID      "Id"
#define MANUFACTURER_NAME    "Name"
#define MANUFACTURER_COUNTRY "Country"

#define DEALERSHIP_ID        "Id"
#define DEALERSHIP_NAME      "Name"
#define DEALERSHIP_ADDRESS   "Address"

#define CUSTOMER_ID          "Id"
#define CUSTOMER_FNAME       "FName"
#define CUSTOMER_LNAME       "LName"
#define CUSTOMER_CONTACTS    "Contacts"

#define SALE_ID              "Id"
#define SALE_DATE            "Date"
#define SALE_DEALER          "Dealer"
#define SALE_CUSTOMER        "Customer"
#define SALE_VEHICLE         "Vehicle"
#define SALE_AMOUNT          "Amount"

#endif // DBNAMES_H

