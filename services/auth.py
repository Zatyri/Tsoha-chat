from db import addUserToDatabase, checkIfUserExcistsinDatabase, getUsersPassword
from models import User
from werkzeug.security import check_password_hash


def checkIfUserExists(user: str) -> bool:
  return checkIfUserExcistsinDatabase(user)
  
def addUser(user: User) -> bool:
  return addUserToDatabase(user)

def userLogin(username: str, password: str) -> bool:
   usersPassword = getUsersPassword(username)   
   return check_password_hash(usersPassword, password)