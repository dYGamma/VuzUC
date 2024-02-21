#include "manufacturerdialog.h"
#include "ui_manufacturerdialog.h"

#include "dbmanager.h"
#include "mainwindow.h"

// конструктор
ManufacturerDialog::ManufacturerDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ManufacturerDialog) {
    ui->setupUi(this);

    connect(ui->btnOk, SIGNAL(clicked()), this, SLOT(onBtnOkClicked()));
    connect(ui->btnCancel, SIGNAL(clicked()), this, SLOT(onBtnCancelClicked()));
}

// деструктор
ManufacturerDialog::~ManufacturerDialog() {
    delete ui;
}

// слоты для кнопок ОК и отмена
void ManufacturerDialog::onBtnOkClicked() {
    // Получаем значения из полей ввода
    QString name = ui->txtName->text().trimmed();
    QString country = ui->txtCountry->text().trimmed();

    // Проверка наличия данных в полях
    if (name.isEmpty() || country.isEmpty()) {
        // Выводим сообщение об ошибке
        QMessageBox::critical(this, "Ошибка", "Пожалуйста, заполните все поля.");
        return;
    }

    // Создаем объект Manufacturer
    Manufacturer m;
    m.name = name;
    m.country = country;

    // Выполняем операции добавления в базу данных и обновления таблицы
    DbManager::instance().insertManufacturer(&m);
    ((MainWindow*)parent())->updateTable();

    // Закрываем диалоговое окно
    this->close();
}

void ManufacturerDialog::onBtnCancelClicked() {
    // Закрываем диалоговое окно
    this->close();
}
