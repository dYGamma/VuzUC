#include "vehicledialog.h"
#include "ui_vehicledialog.h"

#include <QDebug>
#include <QMessageBox>  // Добавьте этот заголовочный файл для использования QMessageBox
#include "dbmanager.h"
#include "mainwindow.h"
#include <QComboBox>
// конструктор
VehicleDialog::VehicleDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::VehicleDialog) {
    ui->setupUi(this);

    // Получаем список производителей из базы данных
    QVector<Manufacturer> manufacturers = DbManager::instance().getManufacturers();
    for (const Manufacturer &manufacturer : manufacturers) {
        ui->cmbMark->addItem(manufacturer.name); // Предполагаем, что у Manufacturer есть поле name
    }

    connect(ui->btnOk, SIGNAL(clicked()), this, SLOT(onBtnOkClicked()));
    connect(ui->btnCancel, SIGNAL(clicked()), this, SLOT(onBtnCancelClicked()));
}

// деструктор
VehicleDialog::~VehicleDialog()
{
    delete ui;
}

// слоты для кнопок
void VehicleDialog::onBtnOkClicked(){
    // Проверка на ввод данных
    if (
        ui->txtModel->text().isEmpty() ||
        ui->txtYear->text().isEmpty() ||
        ui->txtPrice->text().isEmpty() ||
        ui->txtDescription->text().isEmpty() ||
        ui->txtStatus->text().isEmpty()) {
        QMessageBox::critical(this, "Ошибка", "Пожалуйста, заполните все поля.");
        return;
    }

    Vehicle v;
    v.mark = ui->cmbMark->currentText();
    v.model = ui->txtModel->text();

    // Проверка на ввод числовых данных
    bool conversionOk = false;
    v.year = ui->txtYear->text().toInt(&conversionOk);
    if (!conversionOk) {
        QMessageBox::critical(this, "Ошибка", "Некорректный год.");
        return;
    }

    v.price = ui->txtPrice->text().toInt(&conversionOk);
    if (!conversionOk) {
        QMessageBox::critical(this, "Ошибка", "Некорректная цена.");
        return;
    }

    v.description = ui->txtDescription->text();
    v.status = ui->txtStatus->text();

    DbManager::instance().insertVehicle(&v);
    ((MainWindow*)parent())->updateTable();
    this->close();
}

void VehicleDialog::onBtnCancelClicked(){
    this->close();
}
