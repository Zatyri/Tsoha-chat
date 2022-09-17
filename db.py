from app import app
from flask_sqlalchemy import SQLAlchemy
from models import User
import os

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def checkIfUserExcistsinDatabase(username: str) -> bool:
  try:
    sql = "SELECT EXISTS (SELECT * FROM users WHERE users.username = (:username))"
    result = db.session.execute(sql, {"username":username})   
      
    return result.first()[0]    
  except: 
    return False
    
def addUserToDatabase(user: User) -> bool:
  try:
    sql = "INSERT INTO users (username, password, uuid) VALUES (:username, :password, :uuid)"
    db.session.execute(sql, {"username":user.username, "password":user.password, "uuid":user.uuid})
    db.session.commit()
    return True
  except:
    return False

def getUsersPassword(username: str) -> str:
  try:    
    sql = "SELECT password FROM users WHERE users.username = (:username)"
    result = db.session.execute(sql, {"username":username})         
    return result.first()[0]    
  except Exception as e: print(e)
    
   
