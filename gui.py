import sys
import datetime

from main import Database
import pymysql
import random
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QGraphicsScene, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.setWindowTitle("ничто")


    def authoriz(self, wnd):
        dialog = DialogAutorization(wnd)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()


class DialogAutorization(QDialog):
    def __init__(self, wnd, parent = None):
        self.wnd = wnd
        super(DialogAutorization, self).__init__(parent)
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowTitle("Авторизация")
        self.scene = QGraphicsScene(0, 0, 350, 50)
        self.scene.clear()
        self.ui.autorization_btn.clicked.connect(self.autoriz)
        self.ui.captcha_gen.setScene(self.scene)
        self.ui.reboot_btn.clicked.connect(self.gen_captcha)
        self.ui.reboot_btn.setEnabled(False)
        self.ui.line_cap.setEnabled(False)
        self.db = Database()
        self.enter_try = 0
        self.cur_captcha = None
        self.ui.line_pas.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.hide_btn.clicked.connect(self.hide_pas)
        self.hiden = True

    def autoriz(self):
        global login
        global emp_id
        errorcount = 0
        login = self.ui.line_log.text()
        password = self.ui.line_pas.text()
        lock = True

        if self.enter_try>1 and self.ui.line_cap.text() != self.cur_captcha:
            print(self.ui.line_cap.text())
            if errorcount == 0:
                self.error()
                errorcount+=1

            self.enter_try += 1
            lock = False
        else:
            lock = True

        print(lock)

        if self.enter_try >= 2:
            self.gen_captcha()
            self.ui.reboot_btn.setEnabled(True)
            self.ui.line_cap.setEnabled(True)

        if login == '' or password == '':
            if errorcount == 0:
                self.error()
                errorcount += 1

        if login not in self.db.check_login():
            if errorcount == 0:
                self.error()
                errorcount += 1
            self.enter_try += 1
        else:
            aut = self.db.get_log(login)
            autpas = aut[0]
            role = aut[1]
            emp_id = aut[2]
            time = datetime.datetime.now()
            ent_time = time.strftime("%d:%m:%Y %H:%M:%S")
            status ="auth succes"
            self.db.log_his(login,ent_time,status)



            if password != autpas:
                self.enter_try += 1
                if errorcount == 0:
                    self.error()
                    errorcount += 1

            elif lock== True:
                print(lock)
                if role == 'Старший смены' :
                    self.shif_head_open()
                if role == 'Администратор':
                    self.admin_open()
                if role == 'Продавец':
                    self.seller_open()
        errorcount = 0

    def hide_pas(self):
        if self.hiden == True:
            self.hiden = False
            self.ui.line_pas.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.hiden = True
            self.ui.line_pas.setEchoMode(QtWidgets.QLineEdit.Password)

    def gen_captcha(self):
        self.scene.clear()
        symb = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        s_count = 5

        cur_symb = [1, 2, 3, 4, 5]
        x, y = 30, 20
        self.scene.addLine(20, random.randint(10, 40), 300, random.randint(10, 40))
        for i in range(s_count):
            cur_symb[i] = symb[random.randint(0, 61)]
            text = self.scene.addText(f"{cur_symb[i]}")
            x += 40
            text.moveBy(x, y + random.randint(-10, 10))
        self.cur_captcha = ''.join(cur_symb)
        print(self.cur_captcha)

    def error(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка")
        self.mesbox.setText("Ошибка входа")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()
    def shif_head_open(self):
        self.ui.close()
        self.ui = ShiftHeadMenu()
        self.ui.show()
    def admin_open(self):
        self.ui.close()
        self.ui = AdminMenu()
        self.ui.show()
    def seller_open(self):
        self.ui.close()
        self.ui = SellerMenu()
        self.ui.show()

class ShiftHeadMenu(QMainWindow):
    def __init__(self):
        super(ShiftHeadMenu, self).__init__()
        self.ui = uic.loadUi("forms/shift_head.ui", self)
        self.window().setWindowTitle("ShiftHead")
        self.ui.back_btn.clicked.connect(self.exit)
        self.table = self.ui.tableWidget
        self.db = Database()
        self.ui.add_order_btn.clicked.connect(self.add_order)
        self.ui.OrdersTable.clicked.connect(self.orders)
        self.ui.clientTable.clicked.connect(self.clients)
        self.ui.add_client_btn.clicked.connect(self.add_client)

    def orders(self):
        self.table.clear()
        out = self.db.get_ord()
        self.table.setColumnCount(9)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'код заказа', 'дата создания', 'Время заказа', 'Код клиента', 'Код услуги', 'статус',
             'дата закрытия', 'время аренды'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
    def add_order(self):
        dialog = DialogAdd()
        dialog.setWindowTitle("Добавить заказ")
        dialog.show()
        dialog.exec_()
        self.table.clear()
        self.orders()

    def clients(self):
        self.table.clear()
        out = self.db.get_clnt()
        self.table.setColumnCount(6)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'ФИО', 'Паспортные данные', 'Дата рождения', 'Адрес', 'e-mail'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def add_client(self):
        dialog = DialogAddClient()
        dialog.setWindowTitle("Добавить клиента")
        dialog.show()
        dialog.exec_()
        self.table.clear()
        self.clients()


    def exit(self):
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

class AdminMenu(QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.window().setWindowTitle("Admin")
        self.db = Database()
        self.ui.orders_btn.clicked.connect(self.orders)
        self.ui.expenses_btn.clicked.connect(self.services)
        self.ui.history_btn.clicked.connect(self.history)
        self.ui.add_serv.clicked.connect(self.add_service)
        self.ui.back_btn.clicked.connect(self.exit)
        self.table = self.ui.tableWidget

    def orders(self):
        self.table.clear()
        out = self.db.get_ord()
        self.table.setColumnCount(9)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'код заказа', 'дата создания','Время заказа','Код клиента','Код услуги','статус', 'дата закрытия','время аренды'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
    def services(self):
        self.table.clear()
        out = self.db.get_serv()
        self.table.setColumnCount(4)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название услуги', 'Код услуги', 'Цена за час'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
    def history(self):
        self.table.clear()
        out = self.db.get_his()
        self.table.setColumnCount(5)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Вход', 'Выход', 'Успешность входа', 'Сотрудник'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)
    def add_service(self):
        dialog = DialogAddServ()
        dialog.setWindowTitle("Добавить услугу")
        dialog.show()
        dialog.exec_()
        self.table.clear()
        self.orders()


    def exit(self):
        time = datetime.datetime.now()
        ent_time = time.strftime("%d:%m:%Y %H:%M:%S")
        status = "session ended"
        self.db.logout_his(login, ent_time, status)
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()


class SellerMenu(QMainWindow):
    def __init__(self):
        super(SellerMenu, self).__init__()
        self.ui = uic.loadUi("forms/seller.ui", self)
        self.window().setWindowTitle("Seller")
        self.table = self.ui.order_table
        self.db = Database()
        self.ui.order_add_btn.clicked.connect(self.add_order)
        self.table = self.ui.order_table
        self.ui.back_btn.clicked.connect(self.exit)
        self.ui.add_clnt.clicked.connect(self.add_client)
        self.orders()

    def exit(self):
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

    def orders(self):
        self.table.clear()
        out = self.db.get_ord()
        self.table.setColumnCount(9)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'код заказа', 'дата создания','Время заказа','Код клиента','Код услуги','статус', 'дата закрытия','время аренды'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def add_order(self):
        dialog = DialogAdd()
        dialog.setWindowTitle("Добавить заказ")
        dialog.show()
        dialog.exec_()
        self.table.clear()
        self.orders()

    def add_client(self):
        dialog = DialogAddClient()
        dialog.setWindowTitle("Добавить клиента")
        dialog.show()
        dialog.exec_()
        self.table.clear()
        self.orders()






class DialogAdd(QDialog):
    def __init__(self):
        super(DialogAdd, self).__init__()
        self.ui = uic.loadUi("forms/add_order.ui", self)
        self.setWindowTitle("Добавить")
        self.db = Database()
        self.ui.add_btn_2.clicked.connect(self.add)
        self.build_combobox_clients()
        self.build_combobox_serv()

    def add(self):
        self.datetime = datetime.datetime.now()
        self.client = self.comboClient.currentText()
        self.client_code = str(self.db.get_clnt_code(self.client))
        self.date = str(datetime.date.today())
        self.code = str(self.client_code) + "/" + str(self.date)
        self.service = self.comboServ.currentText()
        self.service_code = self.db.get_serv_code(self.service)
        self.time= str(self.datetime.strftime("%H:%M"))
        self.status = self.ui.order_status.text()
        self.close_date= self.ui.end_date.text()
        self.rent_time=self.ui.use_time.text()
        self.db.add_ord(self.code, self.date, self.time, self.client_code, self.service_code, self.status, self.close_date,self.rent_time, emp_id)
        self.ui.close()
    def build_combobox_clients(self):
        """
        Добавление списка клиентов в ComboBox
        :return:
        """
        clients = self.db.get_clnt_name()
        self.comboClient.clear()
        if self.comboClient is not None:
            self.comboClient.addItems(clients)

    def build_combobox_serv(self):
        """
        Добавление списка услуг в ComboBox
        :return:
        """
        services = self.db.get_serv_title()
        self.comboServ.clear()
        if self.comboServ is not None:
            self.comboServ.addItems(services)

class DialogAddClient(QDialog):
    def __init__(self):
        super(DialogAddClient, self).__init__()
        self.ui = uic.loadUi("forms/add_client.ui", self)
        self.setWindowTitle("Добавить")
        self.db = Database()
        self.ui.add_btn_2.clicked.connect(self.add_cln)


    def add_cln(self):
        self.name = self.ui.name_line.text()
        self.p_data = self.ui.passport_line.text()
        self.birth = self.birth_line.text()
        self.addres = self.addres_line.text()
        self.mail = self.ui.email_line.text()
        self.db.add_clnt(self.name, self.p_data, self.birth, self.addres, self.mail)


class DialogAddServ(QDialog):
    def __init__(self):
        super(DialogAddServ, self).__init__()
        self.ui = uic.loadUi("forms/add_serv.ui", self)
        self.setWindowTitle("Добавить")
        self.db = Database()
        self.ui.add_btn_2.clicked.connect(self.add)

    def add(self):
        self.title = self.ui.serv_title.text()
        self.code = self.ui.serv_code.text()
        self.price = self.ui.serv_price.text()
        self.db.add_serv(self.title, self.code, self.price)
        self.ui.close()



class Builder:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wnd = MainWindow()
        self.auth()

    def auth(self):
        self.wnd.authoriz(self.wnd)
        self.app.exec()

if __name__ == '__main__':
    B = Builder()
