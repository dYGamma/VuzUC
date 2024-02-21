
#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QDebug>
#include <iostream>
#include <QMessageBox>

#include "dbnames.h"
#include "dbmanager.h"
#include "vehicledialog.h"
#include "manufacturerdialog.h"
#include "dealershipdialog.h"
#include "customerdialog.h"
#include "saledialog.h"

// конструктор
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // подключаемся к БД
    DbManager::instance().connectToDB();

    // создаем модель данных
    model = new QSqlTableModel;



    // подключение сигналов к слотам
    connect(ui->tabWidget, SIGNAL(currentChanged(int)), this, SLOT(tabSelected()));

    connect(ui->btnAddVehicle, SIGNAL(clicked()), this, SLOT(onBtnAddVehicleClicked()));
    connect(ui->btnRemoveVehicle, SIGNAL(clicked()), this, SLOT(onBtnRemoveVehicleClicked()));

    connect(ui->btnAddManufacturer, SIGNAL(clicked()), this, SLOT(onBtnAddManufacturerClicked()));
    connect(ui->btnRemoveManufacturer, SIGNAL(clicked()), this, SLOT(onBtnRemoveManufacturerClicked()));

    connect(ui->btnAddCustomer, SIGNAL(clicked()), this, SLOT(onBtnAddCustomerClicked()));
    connect(ui->btnRemoveCustomer, SIGNAL(clicked()), this, SLOT(onBtnRemoveCustomerClicked()));

    connect(ui->btnAddDealership, SIGNAL(clicked()), this, SLOT(onBtnAddDealershipClicked()));
    connect(ui->btnRemoveDealership, SIGNAL(clicked()), this, SLOT(onBtnRemoveDealershipClicked()));

    connect(ui->btnAddSale, SIGNAL(clicked()), this, SLOT(onBtnAddSaleClicked()));
    connect(ui->btnRemoveSale, SIGNAL(clicked()), this, SLOT(onBtnRemoveSaleClicked()));

    updateTable();

}

// деструктор
MainWindow::~MainWindow() {
    delete model;
    delete ui;
}

// слот смены вкладки
void MainWindow::tabSelected(){
    updateTable();
}

// метод обновления таблиц
void MainWindow::updateTable(){
    if(ui->tabWidget->currentIndex()==0){
        model->setTable(VEHICLES_TABLE);
        model->select();
        ui->tableVehicle->setModel(model);
    }

    if(ui->tabWidget->currentIndex()==1){
        model->setTable(MANUFACTURERS_TABLE);
        model->select();
        ui->tableManufacturers->setModel(model);
    }

    if(ui->tabWidget->currentIndex()==2){
        model->setTable(DEALERSHIPS_TABLE);
        model->select();
        ui->tableDealerships->setModel(model);
    }

    if(ui->tabWidget->currentIndex()==3){
        model->setTable(CUSTOMERS_TABLE);
        model->select();
        ui->tableCustomers->setModel(model);
    }

    if(ui->tabWidget->currentIndex()==4){
        QSqlQuery q = DbManager::instance().getSales();
        QSqlQueryModel *model = new QSqlQueryModel();
        model->setQuery(std::move(q));
        ui->tableSales->setModel(model);
    }
}

// слоты для кнопок добавить и удалить
void MainWindow::onBtnAddVehicleClicked(){
    VehicleDialog* dialog = new VehicleDialog(this);
    dialog->show();
}

void MainWindow::onBtnRemoveVehicleClicked(){
    int selected_row_index = ui->tableVehicle->currentIndex().row();
    if(selected_row_index < 0)
        return;

    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Подтверждение удаления",
                                  "Вы уверены, что хотите удалить эту запись?",
                                  QMessageBox::Yes|QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        model->removeRows(selected_row_index, 1);
        updateTable();
    } else {
        // Если пользователь выбрал "Нет", удаление не происходит
        qDebug() << "Удаление отменено";
    }
}

void MainWindow::onBtnAddManufacturerClicked(){
    ManufacturerDialog* dialog = new ManufacturerDialog(this);
    dialog->show();
}
void MainWindow::onBtnRemoveManufacturerClicked(){
    int selected_row_index = ui->tableManufacturers->currentIndex().row();
    if(selected_row_index < 0)
        return;

    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Подтверждение удаления",
                                  "Вы уверены, что хотите удалить эту запись?",
                                  QMessageBox::Yes|QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        model->removeRows(selected_row_index, 1);
        updateTable();
    } else {
        qDebug() << "Удаление отменено";
    }
}


void MainWindow::onBtnAddCustomerClicked(){
    CustomerDialog* dialog = new CustomerDialog(this);
    dialog->show();
}
void MainWindow::onBtnRemoveCustomerClicked(){
    int selected_row_index = ui->tableCustomers->currentIndex().row();
    if(selected_row_index < 0)
        return;

    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Подтверждение удаления",
                                  "Вы уверены, что хотите удалить эту запись?",
                                  QMessageBox::Yes|QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        model->removeRows(selected_row_index, 1);
        updateTable();
    } else {
        qDebug() << "Удаление отменено";
    }
}

void MainWindow::onBtnAddDealershipClicked(){
    DealershipDialog* dialog = new DealershipDialog(this);
    dialog->show();
}
void MainWindow::onBtnRemoveDealershipClicked(){
    int selected_row_index = ui->tableDealerships->currentIndex().row();
    if(selected_row_index < 0)
        return;

    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Подтверждение удаления",
                                  "Вы уверены, что хотите удалить эту запись?",
                                  QMessageBox::Yes|QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        model->removeRows(selected_row_index, 1);
        updateTable();
    } else {
        qDebug() << "Удаление отменено";
    }
}
void MainWindow::onBtnAddSaleClicked(){
    SaleDialog* dialog = new SaleDialog(this);
    dialog->show();
}
void MainWindow::onBtnRemoveSaleClicked(){
    int selected_row_index = ui->tableSales->currentIndex().row();
    if(selected_row_index < 0)
        return;

    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Подтверждение удаления",
                                  "Вы уверены, что хотите удалить эту запись?",
                                  QMessageBox::Yes|QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        model->removeRows(selected_row_index, 1);
        updateTable();
    } else {
        qDebug() << "Удаление отменено";
    }
}

