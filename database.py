import sqlite3

def start():
    con = sqlite3.connect('schedule.db')
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users 
        (username TEXT)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS courses
        (name TEXT)'''
    )


    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
        (name TEXT,
        course_id INTEGER,
        due_date DATE,
        priority INTEGER,
        user_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id),
        FOREIGN KEY(user_id) REFERENCES users(id))'''
    )
    
    cur.execute('''CREATE TABLE IF NOT EXISTS settings
        (name TEXT,
        value TEXT)'''
    )
    
    con.commit()
    return con, cur

def lastrowid(cur):
    id = cur.execute("SELECT last_insert_rowid()")
    return id.fetchone()[0]
    

# @param data: a list of tuples
def insert(con, cur, table, column_names, data):
    query = "INSERT INTO {} ".format(table)
    
    if column_names is not None:
        query += "({}) ".format(",".join(column_names))

    query += "VALUES ({})".format(",".join(["?"] * len(data[0])))
    # print("query: {}".format(query))
    # print("data: {}".format(data))
    cur.executemany(query, data)
    con.commit()


def select(cur, table, column_names, where_clause, where_data):
    query = "SELECT {} FROM {} ".format(",".join(column_names), table)
    if where_clause is not None:
        query += "WHERE {} ".format(where_clause)
    cur.execute(query, where_data)
    return cur.fetchall()

def terminate(con):
    con.close()