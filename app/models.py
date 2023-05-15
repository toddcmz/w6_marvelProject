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
    teams = db.relationship('TeamsTable', backref='user', lazy=True)

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

# note we need a new relationship line for every foreign key we add. that's interesting.
class HeroTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heroName = db.Column(db.String(40))
    sigAbility1 = db.Column(db.String(50))
    sigAbility2 = db.Column(db.String(50))
    strStat = db.Column(db.Integer)
    magStat = db.Column(db.Integer)
    intStat = db.Column(db.Integer)
    conStat = db.Column(db.Integer)
    resStat = db.Column(db.Integer)
    teams1 = db.relationship('TeamsTable', backref='hero1', lazy=True, foreign_keys='TeamsTable.hero1_id')
    teams2 = db.relationship('TeamsTable', backref='hero2', lazy=True, foreign_keys='TeamsTable.hero2_id')
    teams3 = db.relationship('TeamsTable', backref='hero3', lazy=True, foreign_keys='TeamsTable.hero3_id')
    
    def __repr__(self):
        return f'Hero: {self.heroName}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

class TeamsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(100))
    teamStr = db.Column(db.Integer)
    teamMag = db.Column(db.Integer)
    teamInt = db.Column(db.Integer)
    teamCon = db.Column(db.Integer)
    teamRes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    hero1_id = db.Column(db.Integer, db.ForeignKey('hero_table.id'))
    hero2_id = db.Column(db.Integer, db.ForeignKey('hero_table.id'))
    hero3_id = db.Column(db.Integer, db.ForeignKey('hero_table.id'))
    

    def __repr__(self):
        return f'Team: {self.teamName}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

