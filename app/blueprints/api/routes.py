from flask import request, jsonify
from . import bp
from app.models import User, TeamsTable, HeroTable
from app.blueprints.api.helpers import token_required

# fill in all the get stuff code

# verify a user
@bp.post('/verifyuser')
def api_verify_user():
    content = request.json
    thisUsername = content['username']
    thisPassword = content['password']
    thisUser = User.query.filter_by(username=thisUsername).first()
    if thisUser and thisUser.check_password(thisPassword):
        return jsonify([{'user token': thisUser.token}])
    return jsonify([{'message':'Invalid credentials supplied'}]), 404

# register a user
@bp.post('/newuser')
def api_new_user():
    content = request.json
    thisFirstName = content['first_name']
    thisLastName = content['last_name']
    thisUsername = content['username'] # written like this assuming we're keying into a passed in json obj
    thisEmail = content['email'] # again, this is all predicated on user posting a json file here.
    thisPassword = content['password']
    thisUserCheck = User.query.filter_by(username=thisUsername).first()
    if thisUserCheck:
        return jsonify([{'message':'Username taken, try again.'}])
    thisEmailCheck = User.query.filter_by(email=thisEmail).first()
    if thisEmailCheck:
        return jsonify([{'message':'Email taken, try again.'}])
    thisNewUser = User(first_name = thisFirstName, last_name=thisLastName, email = thisEmail, username=thisUsername)
    thisNewUser.password = thisNewUser.hash_password(thisPassword)
    thisNewUser.add_token()
    thisNewUser.commit()
    return jsonify([{'message': f"{thisNewUser.username} registered"}])

# receive all teams
@bp.get('/allteams')
@token_required
def api_allteams(thisUser):
    result = []
    # add to this list all posts in database
    theseTeams = TeamsTable.query.all() # .all() is returning all posts, where is post is a class
    for eachTeam in theseTeams:
        result.append({'id': eachTeam.id,
                       'teamName':eachTeam.teamName,
                       'teamStr': eachTeam.teamStr,
                       'teamMag': eachTeam.teamMag,
                       'teamInt': eachTeam.teamInt,
                       'teamCon': eachTeam.teamCon,
                       'teamRes': eachTeam.teamRes,
                       'user_id': eachTeam.user_id,
                       'hero1_id': eachTeam.hero1_id,
                       'hero2_id': eachTeam.hero2_id,
                       'hero3_id': eachTeam.hero3_id})
    return jsonify(result), 200 # this 200 is returning a "success" status

# receive all teams from a single user
@bp.get('/teams/<username>')
@token_required
def user_teams(thisUser, username):
    thisUser = User.query.filter_by(username=username).first().user_id
    if thisUser: # if they give us a username we query for it, if there's no match then the username give was invalid
        theseTeams = TeamsTable.query.filter_by(user_id=thisUser)
        result=[]
        for eachTeam in theseTeams:
            result.append({'id': eachTeam.id,
                        'teamName':eachTeam.teamName,
                        'teamStr': eachTeam.teamStr,
                        'teamMag': eachTeam.teamMag,
                        'teamInt': eachTeam.teamInt,
                        'teamCon': eachTeam.teamCon,
                        'teamRes': eachTeam.teamRes,
                        'user_id': eachTeam.user_id,
                        'hero1_id': eachTeam.hero1_id,
                        'hero2_id': eachTeam.hero2_id,
                        'hero3_id': eachTeam.hero3_id})
        return jsonify(result), 200 # this 200 is returning a "success" status
    return jsonify([{'message':"user was not found"}]), 401

# make a new team
@bp.post('/newTeam')
@token_required
def make_newteam(thisUser):
    try:
        # receive post data
        thisContent = request.json
        thisHero1 = HeroTable.query.filter_by(heroName = thisContent.get('hero1')).first()
        thisHero2 = HeroTable.query.filter_by(heroName = thisContent.get('hero2')).first()
        thisHero3 = HeroTable.query.filter_by(heroName = thisContent.get('hero3')).first()
        # add up all stats
        totalStr = thisHero1.strStat + thisHero2.strStat + thisHero3.strStat
        totalMag = thisHero1.magStat + thisHero2.magStat + thisHero3.magStat
        totalInt = thisHero1.intStat + thisHero2.intStat + thisHero3.intStat
        totalCon = thisHero1.conStat + thisHero2.conStat + thisHero3.conStat
        totalRes = thisHero1.resStat + thisHero2.resStat + thisHero3.resStat
        thisTeamName = thisContent.get('teamName')
        thisUserId = thisUser.user_id
        h1_id = thisHero1.id
        h2_id = thisHero2.id
        h3_id = thisHero3.id
        # give stat penalty if there are any repeat heroes
        if h1_id == h2_id or h1_id == h3_id or h2_id == h3_id:
            totalStr -= 25
            totalMag -= 25
            totalInt -= 25
            totalCon -= 25
            totalRes -= 25
            thisTeamName = thisTeamName+' (Soul-Stretch Debuff)'
            
        thisNewTeam = TeamsTable(teamName=thisTeamName, 
                                 teamStr=totalStr, teamMag=totalMag, 
                                 teamInt=totalInt, teamCon=totalCon, 
                                 teamRes=totalRes, user_id=thisUserId,
                                 hero1_id=h1_id, hero2_id=h2_id, hero3_id=h3_id)
        # commit post
        thisNewTeam.commit()
        # return message
        return jsonify([{'message':'Team Created', 'teamName':thisNewTeam.teamName}]), 200
    except:
        return jsonify([{'message': 'invalid form data for new post'}]), 401