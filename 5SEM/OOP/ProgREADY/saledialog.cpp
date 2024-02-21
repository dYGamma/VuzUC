#include "saledialog.h"
#include "ui_saledialog.h"

#include <QSqlTableModel>
#include <QTableView>
#include <QtSql>
#include <QAbstractItemView>
#include <QMessageBox>  // Добавьте этот заголовочный файл для использования QMessageBox

#include "dbmanager.h"
#include "mainwindow.h"
#include "dbnames.h"

// конструктор
SaleDialog::SaleDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SaleDialog) {
    ui->setupUi(this);

    // создаем модель
    QSqlQueryModel *model1 = new QSqlQueryModel;
    // передаем в модель текст sql запроса
    model1->setQuery("SELECT " CUSTOMER_ID ", " CUSTOMER_LNAME " FROM " CUSTOMERS_TABLE);
    // устанавливаем столбцы
    model1->setHeaderData(0,Qt::Horizontal, tr(CUSTOMER_ID));
    model1->setHeaderData(1, Qt::Horizontal, tr(CUSTOMER_LNAME));
    // создаем таблицу, которая будет отображаться в комбобоксе
    QTableView *view1 = new QTableView;
    // настраиваем таблицу
    view1->setSelectionBehavior(QAbstractItemView::SelectRows);
    view1->setSelectionMode(QAbstractItemView::SingleSelection);
    view1->showColumn(1);
    // передаем модель и таблицу в комбобокс
    ui->cbCustomer->setModel(model1);
    ui->cbCustomer->setView(view1);

    QSqlQueryModel *model2 = new QSqlQueryModel;
    model2->setQuery("SELECT " VEHICLE_ID ", " VEHICLE_MARK ", " VEHICLE_MODEL " FROM " VEHICLES_TABLE);
    model2->setHeaderData(0,Qt::Horizontal, tr(VEHICLE_ID));
    model2->setHeaderData(1, Qt::Horizontal, tr(VEHICLE_MARK));
    model2->setHeaderData(2, Qt::Horizontal, tr(VEHICLE_MODEL));
    QTableView *view2 = new QTableView;
    view2->setSelectionBehavior(QAbstractItemView::SelectRows);
    view2->setSelectionMode(QAbstractItemView::SingleSelection);
    view2->setColumnHidden(0, true);
    ui->cbVehicle->setModel(model2);
    ui->cbVehicle->setView(view2);

    QVector<Dealership> dealerships = DbManager::instance().getDealerships();
        for (const Dealership &dealership : dealerships) {
            ui->cmbDealer->addItem(dealership.name, dealership.id); // Предполагаем, что у Dealership есть поля name и id
        }
    connect(ui->btnOk, SIGNAL(clicked()), this, SLOT(onBtnOkClicked()));
    connect(ui->btnCancel, SIGNAL(clicked()), this, SLOT(onBtnCancelClicked()));
}

SaleDialog::~SaleDialog()
{
    delete ui;
}

void SaleDialog::onBtnOkClicked(){
    // Проверка на ввод данных
    if (ui->dateEdit->date().isNull() ||
        ui->cmbDealer->currentText().isEmpty() ||
        ui->cbCustomer->currentText().isEmpty() ||
        ui->cbVehicle->currentText().isEmpty() ||
        ui->txtAmount->text().isEmpty()) {
        QMessageBox::critical(this, "Ошибка", "Пожалуйста, заполните все поля.");
        return;
    }

    Sale s;
    s.date = ui->dateEdit->date();
    s.dealer = ui->cmbDealer->currentText();

    // Проверка на ввод числовых данных
    bool conversionOk = false;
    s.customer = ui->cbCustomer->currentText().toInt(&conversionOk);
    if (!conversionOk) {
        QMessageBox::critical(this, "Ошибка", "Некорректный ID клиента.");
        return;
    }

    s.vehicle = ui->cbVehicle->currentText().toInt(&conversionOk);
    if (!conversionOk) {
        QMessageBox::critical(this, "Ошибка", "Некорректный ID транспортного средства.");
        return;
    }

    s.amount = ui->txtAmount->text().toInt(&conversionOk);
    if (!conversionOk) {
        QMessageBox::critical(this, "Ошибка", "Некорректная сумма.");
        return;
    }

    DbManager::instance().insertSale(&s);
    ((MainWindow*)parent())->updateTable();
    this->close();
}

void SaleDialog::onBtnCancelClicked(){
    this->close();
}
