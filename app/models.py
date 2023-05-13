from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from secrets import token_urlsafe

@login.user_loader # this is built in to our instance of our login manager instanced in our overall init
def load_user(user_id): # now we're going to get our user by our passed in ID, looking it up in table
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    token = db.Column(db.String)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # come back to this - not clear exactly how this realtionsihp will get implemented: heroes = db.relationship('BookList', backref='reader', lazy=True)

    def __repr__(self):
        return f'User {self.username}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        return generate_password_hash(password)
    
    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    def add_token(self):
        setattr(self,'token', token_urlsafe(32) )
    
    def get_id(self): # this gets called automatically by flask_login when needed
        return str(self.user_id)