import database as db

class Schedule:
    def __init__(self):
        con, cur = db.start()
        
    def __del__(self):
        db.terminate(con)