import database as db

con, cur = db.start()
db.terminate(con)