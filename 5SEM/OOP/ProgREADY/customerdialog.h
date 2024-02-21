#ifndef CUSTOMERDIALOG_H
#define CUSTOMERDIALOG_H

#include <QDialog>

namespace Ui {
class CustomerDialog;
}

// класс формы добавления покупателя
class CustomerDialog : public QDialog
{
    Q_OBJECT

public:
    // конструктор
    explicit CustomerDialog(QWidget *parent = nullptr);
    // деструктор
    ~CustomerDialog();

private:
    // указатель на ui
    Ui::CustomerDialog *ui;

private slots:
    // слот кнопки ОК
    void onBtnOkClicked();
    // слот кнопки отмена
    void onBtnCancelClicked();
};

#endif // CUSTOMERDIALOG_H
