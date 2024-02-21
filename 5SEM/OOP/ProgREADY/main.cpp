#include "mainwindow.h"
#include <QApplication>
#include <QMessageBox>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    // Показываем окно приветствия
    QMessageBox welcomeBox;
    welcomeBox.setText("Добро пожаловать!");
    welcomeBox.setInformativeText("Нажмите \"Start\" для запуска программы или \"Cancel\" для выхода.");
    welcomeBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
    welcomeBox.setDefaultButton(QMessageBox::Ok);

    // Устанавливаем текст на кнопке Ok
    auto okButton = welcomeBox.button(QMessageBox::Ok);
    okButton->setText("Start");

    if (welcomeBox.exec() == QMessageBox::Ok) {
        // Если пользователь нажал "Start" в окне приветствия
        MainWindow w;
        w.show();
        return a.exec();
    } else {
        // Если пользователь нажал "Отмена" в окне приветствия
        return 0;
    }
}
