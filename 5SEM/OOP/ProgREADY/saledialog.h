#ifndef SALEDIALOG_H
#define SALEDIALOG_H

#include <QDialog>
namespace Ui {
class SaleDialog;
}

// класс формы добавления продажи
class SaleDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SaleDialog(QWidget *parent = nullptr);
    ~SaleDialog();

private:
    Ui::SaleDialog *ui;

private slots:
    void onBtnOkClicked();
    void onBtnCancelClicked();
};


#endif // SALEDIALOG_H
