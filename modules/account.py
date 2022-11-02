import sqlite3


class Account:
    def __init__(self, log, pswd):
        self.con = sqlite3.connect('management.db')
        self.login = log
        self.password = pswd
        self.data = self.do()

    def do(self):
        cur = self.con.cursor()
        sql = f"SELECT * FROM workers WHERE login = '{self.login}' and password = '{self.password}'"
        return cur.execute(sql).fetchall()[0]

    def get_name(self):
        return self.data[1]

    def get_surname(self):
        return self.data[2]

    def get_sex(self):
        return self.data[3]

    def get_famstatus(self):
        return self.data[4]

    def get_education(self):
        return self.data[5]

    def get_position(self):
        return self.data[6]

    def get_birthdate(self):
        return self.data[7]

    def get_salary(self):
        return self.data[8]

    def get_login(self):
        return self.data[9]

    def get_password(self):
        return self.data[10]
