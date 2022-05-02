import database as db

class Schedule:
    def __init__(self):
        self.con, self.cur = db.start()
    
    def add_user(self, username):
        db.insert(self.con, self.cur, "users", ["username"], [(username,)])
        self.con.commit()
        return db.lastrowid(self.cur)
    
    def set_current_user(self, user_id):
        db.insert(self.con, self.cur, "settings", ["name", "value"], [("current_user", str(user_id))])
        self.con.commit()
    
    def get_current_user(self):
        current_user = db.select(S.cur, "settings", ["value"], "name=?", ("current_user", ))
        if current_user == []:
            username = input("Enter a username: ")
            user_id = S.add_user(username)
            self.set_current_user(user_id)
            current_user = user_id
        else:
            current_user = int(current_user[0][0])
        username = db.select(S.cur, "users", ["username"], "rowid=?", (current_user,))[0][0]

        return username

    def __del__(self):
        db.terminate(self.con)
    

if __name__ == "__main__":
    S = Schedule()
    username = S.get_current_user()
    print("Welcome, {}!".format(username))
