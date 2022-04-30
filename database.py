import sqlite3

def start():
    con = sqlite3.connect('schedule.db')
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS courses
        (id INTEGER PRIMARY KEY,
        name TEXT)'''
    )


    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
        (id INTEGER PRIMARY KEY,
        name TEXT,
        course_id INTEGER,
        due_date DATE,
        priority INTEGER,
        user_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id),
        FOREIGN KEY(user_id) REFERENCES users(id))''')

    return con, cur

def terminate(con):
    con.close()