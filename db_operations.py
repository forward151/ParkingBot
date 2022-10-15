import sqlite3

def add_user_data(user_data):
    id = user_data['id']
    sn = user_data['surname']
    nm = user_data['name']
    pt = user_data['patronymic']
    cr = user_data['car']

    con = sqlite3.connect("database.db")

    cur = con.cursor()
    data_list = cur.execute('SELECT * FROM users').fetchall()
    for i in data_list:
        if i[0] != id and i[4] == cr:
            return
    cur.execute("UPDATE users SET name = ?, patronymic = ?, surname = ?,"
                "car = ?, status = ? WHERE id = ?", (nm, pt, sn, cr, 6, id))
    con.commit()
    con.close()



def check_user_status(user_id):
    con = sqlite3.connect("database.db")

    cur = con.cursor()

    info = cur.execute('SELECT * FROM users WHERE id=?', (user_id,))
    if info.fetchone() is None:
        cur.execute('INSERT INTO users (id, '
                    'name, '
                    'patronymic, '
                    'surname, '
                    'car, '
                    'status) VALUES (?, ?, ?, ?, ?, ?)', (user_id, None, None, None, None, 1))
        con.commit()
        con.close()
        return 1
    else:
        status = cur.execute('SELECT status FROM users WHERE id=?', (user_id,)).fetchone()[0]
        con.close()
        return status


def change_user_status(user_id, status):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    cur.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
    con.commit()
    con.close()

def take_data(user_id):
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    data = cur.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    con.close()
    return data

# add_user_data({'id': 123, 'name': 'asasdsasda', 'patronymic': 'asdfasdf', 'surname': 'ffkdd', 'car': '123asd'})