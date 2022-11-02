import contextlib
import sqlite3


def search(filterBox, filterEdit):
    con = sqlite3.connect('management.db')

    if not filterEdit:
        return None

    if filterBox == 'Имя':
        sql = f"""SELECT * FROM workers WHERE name LIKE '%{filterEdit}%'"""
        cur = con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        cur.close()
        return data, headers

    elif filterBox == 'Фамилия':
        sql = f"""SELECT * FROM workers WHERE surname LIKE '%{filterEdit}%'"""
        cur = con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        cur.close()
        return data, headers

    elif filterBox == 'Логин':
        sql = f"""SELECT * FROM workers WHERE login LIKE '%{filterEdit}%'"""
        cur = con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        cur.close()
        return data, headers

    elif filterBox == 'ID':
        with contextlib.suppress(ValueError):
            sql = f"""SELECT * FROM workers WHERE id = {int(filterEdit)}"""
            cur = con.cursor()
            data = cur.execute(sql).fetchall()
            headers = cur.description
            cur.close()
            return data, headers
