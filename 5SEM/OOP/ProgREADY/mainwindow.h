
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QMessageBox>
#include <QtSql>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

// класс основного окна
class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    // конструктор
    MainWindow(QWidget *parent = nullptr);
    //деструктор
    ~MainWindow();

    // обновление таблиц
    void updateTable();

private:
    // указатель на UI
    Ui::MainWindow *ui;
    // модель данных
    QSqlTableModel *model;


private slots:
    // слоты для кнопок добавить и удалить
    void onBtnAddVehicleClicked();
    void onBtnRemoveVehicleClicked();

    void onBtnAddManufacturerClicked();
    void onBtnRemoveManufacturerClicked();

    void onBtnAddCustomerClicked();
    void onBtnRemoveCustomerClicked();

    void onBtnAddDealershipClicked();
    void onBtnRemoveDealershipClicked();

    void onBtnAddSaleClicked();
    void onBtnRemoveSaleClicked();

    // слот смены вкладки
    void tabSelected();

};

#endif // MAINWINDOW_H
