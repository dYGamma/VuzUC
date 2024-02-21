#ifndef VEHICLEDIALOG_H
#define VEHICLEDIALOG_H

#include <QDialog>

namespace Ui {
class VehicleDialog;
}

// класс формы добавления транспортного средства
class VehicleDialog : public QDialog
{
    Q_OBJECT

public:
    explicit VehicleDialog(QWidget *parent = nullptr);
    ~VehicleDialog();

private:
    Ui::VehicleDialog *ui;

private slots:
    void onBtnOkClicked();
    void onBtnCancelClicked();
};

#endif // VEHICLEDIALOG_H
