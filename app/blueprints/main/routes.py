from flask import render_template, url_for, flash, redirect
from . import bp
from app.forms import AssembleForm
from app.models import HeroTable, TeamsTable, User
from flask_login import login_required, current_user

@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.jinja', title='Avenger Assembler')

@bp.route('/assemble', methods=['GET', 'POST'])
@login_required
def assemble():
    newAssemblage = AssembleForm()
    if newAssemblage.validate_on_submit():
        # get this user id
        thisUser = User.query.filter_by(username=current_user.username).first()
        # get hero stat totals
        # get hero data for names user picked
        thisHero1 = HeroTable.query.filter_by(heroName = newAssemblage.avenger1.data).first()
        thisHero2 = HeroTable.query.filter_by(heroName = newAssemblage.avenger2.data).first()
        thisHero3 = HeroTable.query.filter_by(heroName = newAssemblage.avenger3.data).first()
        # add up all stats
        totalStr = thisHero1.strStat + thisHero2.strStat + thisHero3.strStat
        totalMag = thisHero1.magStat + thisHero2.magStat + thisHero3.magStat
        totalInt = thisHero1.intStat + thisHero2.intStat + thisHero3.intStat
        totalCon = thisHero1.conStat + thisHero2.conStat + thisHero3.conStat
        totalRes = thisHero1.resStat + thisHero2.resStat + thisHero3.resStat
        # get remaining fields to enter into team table
        thisTeamName = newAssemblage.teamName.data
        thisUserId = thisUser.user_id
        h1_id = thisHero1.id
        h2_id = thisHero2.id
        h3_id = thisHero3.id
        # assign all values to teams table
        thisNewTeam = TeamsTable(teamName=thisTeamName, 
                                 teamStr=totalStr, teamMag=totalMag, 
                                 teamInt=totalInt, teamCon=totalCon, 
                                 teamRes=totalRes, user_id=thisUserId,
                                 hero1_id=h1_id, hero2_id=h2_id, hero3_id=h3_id)
        thisNewTeam.commit()
        flash(f"Team {thisTeamName} add to {current_user.username}'s assemblages.", 'success')
        return redirect(url_for('main.teams', thisUser=current_user.username))

    return render_template('assemble.jinja', title="Assemble a Team", form=newAssemblage)

@bp.route('/teams/<thisUser>')
@login_required
def teams(thisUser):
    thisUserId = User.query.filter_by(username=thisUser).first().user_id
    theseTeams = TeamsTable.query.filter_by(user_id=thisUserId)
    return render_template('myteams.jinja', title='My Teams', teams=theseTeams)