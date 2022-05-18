import sqlite3

def start():
    con = sqlite3.connect('schedule.db')
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS courses
        (name TEXT)'''
    )


    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
        (name TEXT,
        course_id INTEGER,
        due_date DATE,
        priority INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id))'''
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

    query += "VALUES ({})".format(",".join(["?"] * len(data)))
    # print("query: {}".format(query))
    # print("data: {}".format(data))
    cur.execute(query, data)
    con.commit()

def select(cur, table, column_names, where_clause, where_data):
    query = "SELECT {} FROM {} ".format(",".join(column_names), table)
    if where_clause is not None:
        query += "WHERE {} ".format(where_clause)
        cur.execute(query, where_data)
    # print("query: {}".format(query))
    # print("data: {}".format(where_data))
    else:
        cur.execute(query)
    return cur.fetchall()

# column_data is a lis of duples (column_name, value)
def update(con, cur, table, column_data, where_clause, where_data):
    query = "UPDATE {} SET {} ".format(table, ",".join(["{}='{}'".format(column_name, value) for column_name, value in column_data]))
    if where_clause is not None:
        query += "WHERE {} ".format(where_clause)
        cur.execute(query, where_data)
        # print("query: {}".format(query))
    else:
        cur.execute(query)
    con.commit()

def delete(con, cur, table, where_clause, where_data):
    query = "DELETE FROM {} ".format(table)
    if where_clause is not None:
        query += "WHERE {} ".format(where_clause)
        cur.execute(query, where_data)
    else:
        cur.execute(query)
    con.commit()

def terminate(con):
    con.close()