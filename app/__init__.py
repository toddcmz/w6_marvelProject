from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from marvel import Marvel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# Spider-Man (Miles Morales)
# War Machine (Marvel: Avengers Alliance)
# these are used in the dropdown menus when picking heroes
heroChoices = ["Black Panther", "Black Widow", "Captain America", "Doctor Strange", 
               "Hawkeye", "Hulk", "Iron Man", "Loki", "Nick Fury", "Scarlet Witch",
               "Spider-Man", "Thor", "Vision", "War Machine", "Wolverine"]

# this is for getting the marvel api descriptions and images, some names need extra text to query successfully
fullMarvelNames = ["Black Panther", "Black Widow", "Captain America", "Doctor Strange", 
               "Hawkeye", "Hulk", "Iron Man", "Loki", "Nick Fury", "Scarlet Witch",
               "Spider-Man (Miles Morales)", "Thor", "Vision", "War Machine (Marvel: Avengers Alliance)", "Wolverine"]

# get all character descriptions and image urls
myMarvelData = {}
response = Marvel(PUBLIC_KEY = Config.MARVEL_PUBLIC_KEY,
                      PRIVATE_KEY = Config.MARVEL_PRIVATE_KEY)

allChars = response.characters

for thisName in fullMarvelNames:
    thisHeroData = allChars.all(name=thisName)["data"]["results"]
    for ele in thisHeroData:
        thisHeroDesc = ele['description']
        thisImgPath = ele['thumbnail']['path']+".jpg"
        if thisHeroDesc=="":
            thisHeroDesc = "This hero has decided they do not wish to reveal more intimate origin story details."
        myMarvelData[thisName] = [thisHeroDesc,thisImgPath]

login.login_view = 'auth.signin'
login.login_message = 'Anonymous users are not allowed to visit that page. Please log in, first.'
login.login_message_category = 'warning'

from app.blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)
from app.blueprints.main import bp as main_bp
app.register_blueprint(main_bp)
from app.blueprints.api import bp as api_bp
app.register_blueprint(api_bp)

from app import models