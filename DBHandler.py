import DataBase

def AddUser(username, password):
    db = DataBase.ORM()
    for user in db.GetUsersNames():
        if username == user[0]:
            return "TAKEN"
    if db.insert_new_user(username, password):
        return "OK"
    return "ERROR"
def Login(username, password):
    db = DataBase.ORM()
    if (username, password) in db.get_users_passwords():
        return True
    return False
def AddScore(username,score):
    db = DataBase.ORM()
    db.AddScore(username, str(score))

def GetScore(username):
    db = DataBase.ORM()
    score = db.GetScore(username)
    return score[0]

def GetCharacters():
    db = DataBase.ORM()
    characters = db.GetCharacters()
    return characters

def GetCharacter(name):
    db = DataBase.ORM()
    character = db.GetCharacter(name)
    return character

def GetCharactersNames():
    db = DataBase.ORM()
    characters = db.GetCharactersNames()
    return characters

