import sqlite3


def add_user_data(user_data):
    cr = user_data['car']
    nm = user_data['name']
    pt = user_data['patronymic']
    sn = user_data['surname']
    uid = user_data['id']
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    data_list = cur.execute('SELECT * FROM users').fetchall()
    for i in data_list:
        if i[0] != id and i[4] == cr:
            return
    cur.execute("UPDATE users SET name = ?, patronymic = ?, surname = ?,"
                "car = ?, status = ? WHERE id = ?", (nm, pt, sn, cr, 6, uid))
    con.commit()
    con.close()


def clear_data():
    con = sqlite3.connect("database.db")

    cur = con.cursor()
    data_list = cur.execute('SELECT * FROM users').fetchall()
    for i in data_list:
        cur.execute("UPDATE users SET monday = ?, tuesday = ?, wednesday = ?,"
                    "thursday = ?, friday = ? WHERE id = ?", (0, 0, 0, 0, 0, i[0]))
        con.commit()
    con.close()


def add_date_for_user(user_data, day):
    id = user_data['id']

    con = sqlite3.connect("database.db")

    cur = con.cursor()
    if day == 1:
        d = user_data['monday']
        cur.execute("UPDATE users SET monday = ? WHERE id = ?", (d, id))
    if day == 2:
        d = user_data['tuesday']
        cur.execute("UPDATE users SET tuesday = ? WHERE id = ?", (d, id))
    if day == 3:
        d = user_data['wednesday']
        cur.execute("UPDATE users SET wednesday = ? WHERE id = ?", (d, id))
    if day == 4:
        d = user_data['thursday']
        cur.execute("UPDATE users SET thursday = ? WHERE id = ?", (d, id))
    if day == 5:
        d = user_data['friday']
        cur.execute("UPDATE users SET friday = ? WHERE id = ?", (d, id))
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
                    'status,'
                    'monday,'
                    'tuesday,'
                    'wednesday,'
                    'thursday,'
                    'friday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, None, None, None, None, 1, False, False, False, False, False))
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
    data = {'id': data[0], 'name': data[1], 'patronymic': data[2], 'surname': data[3], 'car': data[4], 'monday': data[6], 'tuesday': data[7], 'wednesday': data[8], 'thursday': data[9], 'friday': data[10]}
    return data
