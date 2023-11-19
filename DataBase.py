import sqlite3

class ORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"
    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('Data.db')
        self.current=self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_tables(self):
        self.open_DB()
        sql = "CREATE TABLE Users (username TEXT, password TEXT, score INTEGER)"
        self.current.execute(sql)
        sql = "CREATE TABLE Characters (name TEXT, shot TEXT, ult TEXT, shot_damage INTEGER, ult_damage INTEGER)"
        self.current.execute(sql)
        self.commit()
        self.close_DB()
    def stam(self):
        self.open_DB()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"
        result = self.current.execute(sql)
        print(result)
        for ans in result:
            print(ans)
        self.close_DB()

    def insert_new_user(self, username, password):
        self.open_DB()
        sql = "INSERT INTO Users (username, password, score) VALUES('"+username+"','"+password+"',0) "
        self.current.execute(sql)
        self.commit()
        self.close_DB()
        return True

    def insert_new_character(self, name, shot, ult, shot_damage, ult_damage):
        self.open_DB()
        sql = "INSERT INTO Characters (name, shot, ult, shot_damage, ult_damage) VALUES('" + name + "','" + shot + "','" + ult + "','" + shot_damage + "','" + ult_damage + "') "
        self.current.execute(sql)
        self.commit()
        self.close_DB()
        return True

    def GetUsersNames(self):
        self.open_DB()
        sql = "SELECT username FROM Users"
        res = self.current.execute(sql)
        usrs = []
        for usr in res:
            usrs.append(usr)
        self.close_DB()
        return usrs

    def AddScore(self, username, amount):
        self.open_DB()
        sql = "UPDATE Users SET score = score + "+amount+" WHERE username = '"+username+"'"
        self.current.execute(sql)
        self.commit()
        self.close_DB()
        return True

    def get_users_passwords(self):
        self.open_DB()
        sql = "SELECT username, password FROM Users"
        res = self.current.execute(sql)
        usrs = []
        for usr in res:
            usrs.append(usr)
        self.close_DB()
        return usrs
    def GetScore(self, username):
        self.open_DB()
        sql = "SELECT score FROM Users WHERE username = '"+username+"'"
        res = self.current.execute(sql)
        score = 0
        for ans in res:
            score = ans
        self.close_DB()
        return score
    def GetCharacters(self):
        self.open_DB()
        sql = "SELECT * FROM Characters"
        res = self.current.execute(sql)
        characters = []
        for ans in res:
            characters.append(ans)
        self.close_DB()
        return characters

    def GetCharactersNames(self):
        self.open_DB()
        sql = "SELECT name FROM Characters"
        res = self.current.execute(sql)
        characters = []
        for ans in res:
            characters.append(ans[0])
        self.close_DB()
        return characters
    def GetCharacter(self, name):
        self.open_DB()
        sql = "SELECT * FROM Characters WHERE name = '"+name+"'"
        res = self.current.execute(sql)
        character = ""
        for ans in res:
            character = ans
        self.close_DB()
        return character




def main_test():

    ORM().insert_new_character("SKELETON", "BONE", "SKULL", "10", "50")
    print(ORM().GetCharacters())
    print(ORM().GetCharactersNames())
    print(ORM().GetCharacter("SKELETON"))



if __name__ == "__main__":
    main_test()