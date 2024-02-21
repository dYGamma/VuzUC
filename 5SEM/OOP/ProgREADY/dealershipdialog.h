#ifndef DEALERSHIPDIALOG_H
#define DEALERSHIPDIALOG_H

#include <QDialog>

namespace Ui {
class DealershipDialog;
}

// класс формы добавления дилерского центра
class DealershipDialog : public QDialog
{
    Q_OBJECT

public:
    explicit DealershipDialog(QWidget *parent = nullptr);
    ~DealershipDialog();

private:
    Ui::DealershipDialog *ui;

private slots:
    void onBtnOkClicked();
    void onBtnCancelClicked();
};

#endif // DEALERSHIPDIALOG_H
