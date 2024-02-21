#include "dealershipdialog.h"
#include "ui_dealershipdialog.h"

#include "dbmanager.h"
#include "mainwindow.h"

DealershipDialog::DealershipDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DealershipDialog) {
    ui->setupUi(this);

    connect(ui->btnOk, SIGNAL(clicked()), this, SLOT(onBtnOkClicked()));
    connect(ui->btnCancel, SIGNAL(clicked()), this, SLOT(onBtnCancelClicked()));
}

DealershipDialog::~DealershipDialog() {
    delete ui;
}

void DealershipDialog::onBtnOkClicked() {
    // Получаем значения из полей ввода
    QString name = ui->txtName->text().trimmed();
    QString address = ui->txtAddress->text().trimmed();

    // Проверка наличия данных в полях
    if (name.isEmpty() || address.isEmpty()) {
        // Выводим сообщение об ошибке
        QMessageBox::critical(this, "Ошибка", "Пожалуйста, заполните все поля.");
        return;
    }

    // Создаем объект Dealership
    Dealership d;
    d.name = name;
    d.address = address;

    // Выполняем операции добавления в базу данных и обновления таблицы
    DbManager::instance().insertDealership(&d);
    ((MainWindow*)parent())->updateTable();

    // Закрываем диалоговое окно
    this->close();
}

void DealershipDialog::onBtnCancelClicked() {
    // Закрываем диалоговое окно
    this->close();
}
