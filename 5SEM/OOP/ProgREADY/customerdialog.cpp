#include "customerdialog.h"
#include "ui_customerdialog.h"

#include "dbmanager.h"
#include "mainwindow.h"

// конструктор
CustomerDialog::CustomerDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::CustomerDialog) {
    // создание UI
    ui->setupUi(this);

    // подключение сигналов к слотам
    connect(ui->btnOk, SIGNAL(clicked()), this, SLOT(onBtnOkClicked()));
    connect(ui->btnCancel, SIGNAL(clicked()), this, SLOT(onBtnCancelClicked()));
}

// деструктор
CustomerDialog::~CustomerDialog()
{
    delete ui;
}

// слот кнопки ОК
void CustomerDialog::onBtnOkClicked(){
    // Получаем значения из полей ввода
    QString firstName = ui->txtFName->text().trimmed();
    QString lastName = ui->txtLName->text().trimmed();
    QString contacts = ui->txtContacts->text().trimmed();

    // Проверка наличия данных в полях
    if (firstName.isEmpty() || lastName.isEmpty() || contacts.isEmpty()) {
        // Выводим сообщение об ошибке
        QMessageBox::critical(this, "Ошибка", "Пожалуйста, заполните все поля.");
        return;
    }

    // Проверка отсутствия цифр в полях "Имя" и "Фамилия"
    QRegularExpression regex("\\d");
    if (regex.match(firstName).hasMatch() || regex.match(lastName).hasMatch()) {
        // Выводим сообщение об ошибке
        QMessageBox::critical(this, "Ошибка", "Некорректное Имя или Фамилия");
        return;
    }

    // Создаем объект Customer
    Customer c;
    c.first_name = firstName;
    c.last_name = lastName;
    c.contacts = contacts;

    // Выполняем операции добавления в базу данных и обновления таблицы
    DbManager::instance().insertCustomer(&c);
    ((MainWindow*)parent())->updateTable();

    // Закрываем диалоговое окно
    this->close();
}

void CustomerDialog::onBtnCancelClicked(){
    // Закрываем диалоговое окно
    this->close();
}
