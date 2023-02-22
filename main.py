import pymysql
import datetime
import mysql
from mysql.connector import connect, Error


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='igora',
        )

    def get_his(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from History')
        his = cursor.fetchall()
        cursor.close()
        return (his)

    def log_his(self, login, time, status):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, %s, NULL, %s, %s)", (time, status, login))
        self.connection.commit()

    def logout_his(self, login, time, status):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, NULL, %s, %s, %s)", (time, status, login))
        self.connection.commit()

    def get_emp(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from employee')
        emps = cursor.fetchall()
        cursor.close()
        return (emps)

    def get_clnt(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from client')
        clnt = cursor.fetchall()
        cursor.close()
        return clnt

    def get_clnt_name(self):
        clients = []
        cursor = self.connection.cursor()
        cursor.execute(f"select cl_name from client")
        clnt = cursor.fetchall()
        cursor.close()
        for i in clnt:
            clients.append(str(i)[2:-3])
        return clients

    def get_clnt_code(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT `cl_Id` FROM client WHERE cl_name='{name}'")
        clnt = cursor.fetchone()
        cursor.close()
        return clnt[0]
    def add_clnt(self, name, data, birth, addres, mail):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO client VALUES (NULL, %s, %s, %s, %s, %s, NULL)", (name, data, birth, addres, mail))
        cursor.close()
        self.connection.commit()

    def get_ord(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from orders')
        ord = cursor.fetchall()
        cursor.close()
        return (ord)

    def add_ord(self, code, date, time, client, serv, status, close_time, rent_time, emp_id):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO orders VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (code, date, time, client, serv, status, close_time, rent_time, emp_id))

        cursor.close()
        self.connection.commit()
    def get_serv(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from services')
        serv = cursor.fetchall()
        cursor.close()
        return serv

    def get_serv_title(self):
        services = []
        cursor = self.connection.cursor()
        cursor.execute(f"select serv_Title from services")
        serv = cursor.fetchall()
        cursor.close()
        for i in serv:
            services.append(str(i)[2:-3])
        return services

    def get_serv_code(self, title):
        cursor = self.connection.cursor()
        cursor.execute(f"select serv_id from services WHERE serv_Title='{title}'")
        serv = cursor.fetchone()
        cursor.close()
        return serv[0]
    def add_serv(self, title, code, price):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO services VALUES (NULL, %s, %s, %s)", (title, code, price))

        cursor.close()
        self.connection.commit()

    def check_login(self):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT login FROM Employee""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        return log

    def get_log(self, login):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT password, Position, emp_ID FROM employee WHERE login = '{login}'""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        return log


if __name__ == '__main__':
    db = Database()
    print(db.get_clnt_name())
