import os
import sqlite3
from hashlib import md5


DATABASE = os.path.join(os.path.dirname(__file__), 'data.db')


'''
--------------------------------
|         table users          |
--------------------------------
| id       | int auto  primary |
--------------------------------
| username | string not null   |
--------------------------------
| password | string not null   |
--------------------------------
| identity | int not null      |
--------------------------------
| mail     | string not null   |
--------------------------------
identity : 1 teacher    0 student
'''


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    sql_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(sql_file, 'r') as f:
        sql = f.read()
        c.executescript(sql)
        conn.commit()
        conn.close()


def add_user(username, password, identity, mail):
    if not isinstance(password, str) or not isinstance(username, str):
        return False
    if identity not in (0, 1):
        return False
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        password = get_md5(password)
        c.execute('INSERT INTO users (username, password, identity, mail) VALUES (?, ?, ?, ?)',
                  (username, password, identity, mail))
        conn.commit()
        c.execute('select last_insert_rowid() from users')
        id = c.fetchone()[0]
        conn.close()
        return id
    except Exception as e:
        print(e)
        return False


def check_password(uid, password):
    try:
        if not isinstance(uid, int):
            uid = int(uid)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute(f"SELECT * FROM users WHERE id = {uid}")
        real_password = c.fetchone()[2]
        conn.close()
        if real_password == get_md5(password):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def change_user(uid, username, password, identity, mail):
    if not isinstance(password, str) or not isinstance(username, str):
        return False
    if identity not in (0, 1):
        return False
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        password = get_md5(password)
        c.execute(
            f'UPDATE users SET username = "{username}", password = "{password}", identity = {identity}, mail = "{mail}" where id = {uid}')
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_identity(uid):
    try:
        if not isinstance(uid, int):
            uid = int(uid)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute(f"SELECT * FROM users WHERE id = {uid}")
        identity = c.fetchone()[3]
        conn.close()
        return identity
    except Exception as e:
        print(e)
        return -1


def get_user_info(uid):
    try:
        if not isinstance(uid, int):
            uid = int(uid)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute(
            f"SELECT id, username, identity, mail FROM users WHERE id = {uid}")
        info = c.fetchone()
        conn.close()
        if info[0] == uid:
            return info
        else:
            return None
    except Exception as e:
        print(e)
        return None


'''
--------------------------------
|         table rooms          |
--------------------------------
| id       | int auto  primary |
--------------------------------
| tid      | int not null      |
--------------------------------
| name     | string not null   |
--------------------------------
| profile  | string not null   |
--------------------------------

foreign key tid references user(id)
'''


def add_room(tid, name, profile):
    if isinstance(tid, int) and isinstance(name, str) and isinstance(profile, str):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys=ON;')
            c.execute('INSERT INTO rooms (tid, name, profile) VALUES (?, ?, ?)',
                      (tid, name, profile))
            conn.commit()
            c.execute('select last_insert_rowid() from rooms')
            rid = c.fetchone()[0]
            conn.close()
            return rid
        except Exception as e:
            print(e)
            return False
    return False


def add_stu(uid, rid):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute('INSERT INTO participants (uid, rid) VALUES (?, ?)',
                  (uid, rid))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_room(uid):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute(f'SELECT rid FROM participants where uid = {uid}')
        res = c.fetchall()
        conn.close()
        return res
    except Exception as e:
        print(e)
        return None


def get_room_info(rid):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys=ON;')
        c.execute(
            f'SELECT rooms.id, users.id, username, name, profile FROM rooms, users WHERE rooms.id={rid} and rooms.tid=users.id')
        res = c.fetchone()
        conn.close()
        return res
    except Exception as e:
        print(e)
        return None


def get_md5(password):
    password = password + '114514'
    return md5(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print('Please import the module instead of running it!')
    # get_info(1)
