from db import addUserToDatabase, checkIfUserExcistsinDatabase, deleteUserFromDB, getUsersPassword, getUsersPasswordAndID, updateUsersPassword
from models import User
from werkzeug.security import check_password_hash, generate_password_hash

def checkIfUserExists(user: str) -> bool:
  return checkIfUserExcistsinDatabase(user)
  
def addUser(user: User) -> bool:
  return addUserToDatabase(user)


def userLogin(username: str, password: str) -> int:
  passwordAndID = getUsersPasswordAndID(username)
  if passwordAndID == None or len(passwordAndID) == 0:
    return -1
  if check_password_hash(passwordAndID[1], password):
    return passwordAndID[0]
  return -1

def deleteUser(userID:int):
  deleteUserFromDB(userID)

def checkUsersPassword(userID:int, givenPassword:str):
  password = getUsersPassword(userID)
  if check_password_hash(password, givenPassword):
    return True
  return False

def changePassword(userID: int, password:str):
  updateUsersPassword(userID, generate_password_hash(password))