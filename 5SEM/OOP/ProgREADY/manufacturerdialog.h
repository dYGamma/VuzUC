#ifndef MANUFACTURERDIALOG_H
#define MANUFACTURERDIALOG_H

#include <QDialog>

namespace Ui {
class ManufacturerDialog;
}

// класс формы добавления производителя
class ManufacturerDialog : public QDialog
{
    Q_OBJECT

public:
    explicit ManufacturerDialog(QWidget *parent = nullptr);
    ~ManufacturerDialog();

private:
    Ui::ManufacturerDialog *ui;

private slots:
    void onBtnOkClicked();
    void onBtnCancelClicked();
};

#endif // MANUFACTURERDIALOG_H
