import app
from app import db


#ROLE_USER = 0
#ROLE_ADMIN = 1

class Todo_list(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String(128), index = True, unique = False)
    title = db.Column(db.String(120), index = True, unique = True)
    uri = db.Column(db.String(128), index = True, unique = False)
    status = db.Column(db.String(20), index = True, unique = False)
class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String)
    password = db.Column(db.String)
  #  def __repr__(self):
   #     return '<Todo_list %r>' % (self.uri)
