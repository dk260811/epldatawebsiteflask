from multiprocessing import process
import os
from pickle import NONE
from telnetlib import PRAGMA_HEARTBEAT, PRAGMA_LOGON
from tkinter.messagebox import NO
import tkinter
  
# C:\Users\Lenovo\pyver\py3105\lib\tty.py qetu e kom hek termios

from cs50 import SQL
from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql import text
from flask import Flask, flash, redirect, render_template, request, session, request, url_for, json, jsonify
from flask_session import Session
from tempfile import mkdtemp
#from sqlalchemy import true
#import sqlalchemy
#from werkzeug.security import check_password_hash, generate_password_hash
#from yaml import serialize, serialize_all
#from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
import random
#import sys, tty, termios

app = Flask(__name__)
#CORS(app)
app.config.from_object(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='favicon.ico'))
#app.add_url_rule('/favicon.ico',redirect_to='/favicon.ico')

#app.listen(process.env.PORT or 3000, function(){
#  console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env)
#})

#db = SQL("sqlite:///PremierLeague.db")
#db = "sqlite:///PremierLeague.db"
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)



def perc(value):
    """Format value as percentage."""
    return f"{value*100:,.1f}%"

def dec(value):
    """Format value as decimal."""
    return f"{value:,.2f}"

def apology():
    """Render message as an apology to user."""
    return render_template("apology.html")

# Render Homepage template
@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")


# Render starting index Table template
@app.route("/index_table", methods=["GET"])
def index_table():

    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
    #engine = create_engine(db)
    #meta = MetaData()
    #conn = engine.connect()
    #data = Table('EPLData', meta, autoload=True, autoload_with=engine)
    #seasons_epl_data = select([data]).distinct(data.c.season_ft)
    #seasons_epl = conn.execute(seasons_epl_data).fetchall()
    #conn.close()
    #engine.dispose()
    return render_template("index_table.html", seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

# Render Table template
@app.route("/table", methods=["POST"])
def table():

    season = request.form.get("season")
    # If condition for Home or Away Table
    if request.form.get("home_away") == None:

        #season = request.form.get("season")
        if season == None:
            return apology()
        seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
        table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY SUM(points_ft) DESC) place, team_ft,SUM(points_ft), SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft), SUM(full_time_goals_scored_ft), SUM(full_time_goals_conceded_ft), SUM(goal_difference_ft), SUM(win_ft), SUM(draw_ft), SUM(loss_ft), season_ft  from EPLData where season_ft = ? GROUP BY team_ft ORDER BY SUM(points_ft) DESC;", season)
        #engine = create_engine(db)
        #meta = MetaData()
        #conn = engine.connect()
        #data = Table('EPLData', meta, autoload=True, autoload_with=engine)
        #seasons_epl_data = select([data]).distinct(data.c.season_ft)
        #seasons_epl = conn.execute(seasons_epl_data).fetchall()
        #conn.close()
        #engine.dispose()
        return render_template("table.html", team_list=[{"place": table_epl[i]["place"],
                                                         "team": table_epl[i]["team_ft"],
                                                         "points":table_epl[i]["SUM(points_ft)"],
                                                         "games":table_epl[i]["SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)"],
                                                         "goals_scored":table_epl[i]["SUM(full_time_goals_scored_ft)"],
                                                         "goals_conceded":table_epl[i]["SUM(full_time_goals_conceded_ft)"],
                                                         "goal_difference":table_epl[i]["SUM(goal_difference_ft)"],
                                                         "win":table_epl[i]["SUM(win_ft)"],
                                                         "draw":table_epl[i]["SUM(draw_ft)"],
                                                         "loss":table_epl[i]["SUM(loss_ft)"],
                                                         "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                         seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

    elif request.form.get("home_away") == "home":
        #season = request.form.get("season")
        if season == None:
            return apology()
        seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
        table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY SUM(points_ft) DESC) place, team_ft,SUM(points_ft), SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft), SUM(full_time_goals_scored_ft), SUM(full_time_goals_conceded_ft), SUM(goal_difference_ft), SUM(win_ft), SUM(draw_ft), SUM(loss_ft), season_ft   from EPLData where season_ft = ? AND home_ft = 'Homegame' GROUP BY team_ft ORDER BY SUM(points_ft) DESC;", season)

        return render_template("table.html", team_list=[{"place": table_epl[i]["place"],
                                                         "team": table_epl[i]["team_ft"],
                                                         "points":table_epl[i]["SUM(points_ft)"],
                                                         "games":table_epl[i]["SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)"],
                                                         "goals_scored":table_epl[i]["SUM(full_time_goals_scored_ft)"],
                                                         "goals_conceded":table_epl[i]["SUM(full_time_goals_conceded_ft)"],
                                                         "goal_difference":table_epl[i]["SUM(goal_difference_ft)"],
                                                         "win":table_epl[i]["SUM(win_ft)"],
                                                         "draw":table_epl[i]["SUM(draw_ft)"],
                                                         "loss":table_epl[i]["SUM(loss_ft)"],
                                                         "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                         seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

    elif request.form.get("home_away") == "away":
        #season = request.form.get("season")
        if season == None:
            return apology()
        seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
        table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY SUM(points_ft) DESC) place, team_ft,SUM(points_ft), SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft), SUM(full_time_goals_scored_ft), SUM(full_time_goals_conceded_ft), SUM(goal_difference_ft), SUM(win_ft), SUM(draw_ft), SUM(loss_ft), season_ft   from EPLData where season_ft = ? AND home_ft = 'Awaygame' GROUP BY team_ft ORDER BY SUM(points_ft) DESC;", season)

        return render_template("table.html", team_list=[{"place": table_epl[i]["place"],
                                                         "team": table_epl[i]["team_ft"],
                                                         "points":table_epl[i]["SUM(points_ft)"],
                                                         "games":table_epl[i]["SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)"],
                                                         "goals_scored":table_epl[i]["SUM(full_time_goals_scored_ft)"],
                                                         "goals_conceded":table_epl[i]["SUM(full_time_goals_conceded_ft)"],
                                                         "goal_difference":table_epl[i]["SUM(goal_difference_ft)"],
                                                         "win":table_epl[i]["SUM(win_ft)"],
                                                         "draw":table_epl[i]["SUM(draw_ft)"],
                                                         "loss":table_epl[i]["SUM(loss_ft)"],
                                                         "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                         seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])


################
@app.route("/index_referee_stats", methods=["GET"])
def index_referee_stats():

    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")

    return render_template("index_referee_stats.html", seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

@app.route("/referee_stats", methods=["POST"])
def referee_stats():

    season = request.form.get("season")
    if season == None:
        return apology()
    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
    table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY SUM(team_fouls_committed_recorded_ft) DESC) place, count(referee_ft), referee_ft, SUM(team_fouls_committed_recorded_ft), CAST(SUM(team_fouls_committed_recorded_ft) AS REAL)/count(referee_ft), SUM(team_yellow_cards_recorded_ft), SUM(team_red_cards_recorded_ft), CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/count(referee_ft), CAST(SUM(team_red_cards_recorded_ft) AS REAL)/count(referee_ft), CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/sum(team_fouls_committed_recorded_ft), season_ft from EPLData where season_ft = ? AND home_ft='Homegame' GROUP BY referee_ft ORDER BY SUM(team_fouls_committed_recorded_ft) DESC;", season)

    return render_template("referee_stats.html", ref_list=[{"games":table_epl[i]["count(referee_ft)"],
                                                            "name":table_epl[i]["referee_ft"],
                                                            "fouls":table_epl[i]["SUM(team_fouls_committed_recorded_ft)"],
                                                            "fouls_per_game":dec(table_epl[i]["CAST(SUM(team_fouls_committed_recorded_ft) AS REAL)/count(referee_ft)"]),
                                                            "yellow_cards":table_epl[i]["SUM(team_yellow_cards_recorded_ft)"],
                                                            "red_cards":table_epl[i]["SUM(team_red_cards_recorded_ft)"],
                                                            "yellow_cards_per_game":dec(table_epl[i]["CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/count(referee_ft)"]),
                                                            "red_cards_per_game":dec(table_epl[i]["CAST(SUM(team_red_cards_recorded_ft) AS REAL)/count(referee_ft)"]),
                                                            "bookings_from_fouls":perc(table_epl[i]["CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/sum(team_fouls_committed_recorded_ft)"]),
                                                            "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                            seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])
###############

##########################
@app.route("/index_stats_averages", methods=["GET"])
def index_stats_averages():

    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")

    return render_template("index_stats_averages.html", seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

@app.route("/stats_averages", methods=["POST"])
def stats_averages():

    season = request.form.get("season")
    if season == None:
        return apology()
    #filter_by = request.form.get("sort_table")
    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")

    table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY CAST(SUM(points_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)) DESC) place, team_ft,CAST(SUM(points_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(win_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(draw_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(loss_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)),CAST(SUM(full_time_goals_scored_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(full_time_goals_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_shots_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_shots_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_shots_on_target_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_shots_on_target_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(full_time_goals_scored_ft) AS REAL)/SUM(team_shots_recorded_ft), CAST(SUM(full_time_goals_conceded_ft) AS REAL)/SUM(team_shots_conceded_ft),CAST(SUM(team_corners_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_corners_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_fouls_committed_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_fouls_committed_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_yellow_cards_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_red_cards_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_red_cards_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)), CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/SUM(team_fouls_committed_recorded_ft), season_ft from EPLData where season_ft =? GROUP BY team_ft ORDER BY SUM(points_ft)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft)) DESC;", season)

    return render_template("stats_averages.html", stats_list_avg=[{"place": table_epl[i]["place"],
                                                            "team":table_epl[i]["team_ft"],
                                                            "ppg":dec(table_epl[i]["CAST(SUM(points_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "w_perc":perc(table_epl[i]["CAST(SUM(win_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "d_perc":perc(table_epl[i]["CAST(SUM(draw_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "l_perc":perc(table_epl[i]["CAST(SUM(loss_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "gpg_recorded":dec(table_epl[i]["CAST(SUM(full_time_goals_scored_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "gpg_conceded":dec(table_epl[i]["CAST(SUM(full_time_goals_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "spg_recorded":dec(table_epl[i]["CAST(SUM(team_shots_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "spg_conceded":dec(table_epl[i]["CAST(SUM(team_shots_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "sotpg_recorded":dec(table_epl[i]["CAST(SUM(team_shots_on_target_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "sotpg_conceded":dec(table_epl[i]["CAST(SUM(team_shots_on_target_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "shot_conversion":perc(table_epl[i]["CAST(SUM(full_time_goals_scored_ft) AS REAL)/SUM(team_shots_recorded_ft)"]),
                                                            "shot_conversion_against":perc(table_epl[i]["CAST(SUM(full_time_goals_conceded_ft) AS REAL)/SUM(team_shots_conceded_ft)"]),
                                                            "cpg_recorded":dec(table_epl[i]["CAST(SUM(team_corners_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "cpg_conceded":dec(table_epl[i]["CAST(SUM(team_corners_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "fpg_recorded":dec(table_epl[i]["CAST(SUM(team_fouls_committed_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "fpg_against":dec(table_epl[i]["CAST(SUM(team_fouls_committed_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "ycpg_recorded":dec(table_epl[i]["CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "ycpg_conceded":dec(table_epl[i]["CAST(SUM(team_yellow_cards_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "rcpg_recorded":dec(table_epl[i]["CAST(SUM(team_red_cards_recorded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "rcpg_conceded":dec(table_epl[i]["CAST(SUM(team_red_cards_conceded_ft) AS REAL)/(SUM(win_ft)+SUM(draw_ft)+SUM(loss_ft))"]),
                                                            "booking_perc":perc(table_epl[i]["CAST(SUM(team_yellow_cards_recorded_ft) AS REAL)/SUM(team_fouls_committed_recorded_ft)"]),
                                                            "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                            seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])
    #return render_template("stats_averages.html")
###################

#######################
@app.route("/index_stats_totals", methods=["GET"])
def index_stats_totals():

    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")

    return render_template("index_stats_totals.html", seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

@app.route("/stats_totals", methods=["POST"])
def stats_totals():

    season = request.form.get("season")
    if season == None:
        return apology()
    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
    table_epl = db.execute("select ROW_NUMBER() OVER(ORDER BY SUM(team_corners_recorded_ft) DESC) place, team_ft,SUM(team_corners_recorded_ft), SUM(team_corners_conceded_ft), SUM(team_shots_recorded_ft), SUM(team_shots_conceded_ft), SUM(team_shots_on_target_recorded_ft), SUM(team_shots_on_target_conceded_ft), SUM(team_fouls_committed_recorded_ft), SUM(team_fouls_committed_conceded_ft), SUM(team_yellow_cards_recorded_ft), SUM(team_yellow_cards_conceded_ft), SUM(team_red_cards_recorded_ft), SUM(team_red_cards_conceded_ft), season_ft from EPLData where season_ft = ? GROUP BY team_ft ORDER BY SUM(team_corners_recorded_ft) DESC;", season)

    return render_template("stats_totals.html", stats_list=[{"place": table_epl[i]["place"],
                                                            "team_ft": table_epl[i]["team_ft"],
                                                            "corners_for": table_epl[i]["SUM(team_corners_recorded_ft)"],
                                                            "corners_against":table_epl[i]["SUM(team_corners_conceded_ft)"],
                                                            "shots_for":table_epl[i]["SUM(team_shots_recorded_ft)"],
                                                            "shots_agains":table_epl[i]["SUM(team_shots_conceded_ft)"],
                                                            "shots_on_target_for":table_epl[i]["SUM(team_shots_on_target_recorded_ft)"],
                                                            "shots_on_target_against":table_epl[i]["SUM(team_shots_on_target_conceded_ft)"],
                                                            "fouls_commited":table_epl[i]["SUM(team_fouls_committed_recorded_ft)"],
                                                            "fouls_against":table_epl[i]["SUM(team_fouls_committed_conceded_ft)"],
                                                            "yellow_cards":table_epl[i]["SUM(team_yellow_cards_recorded_ft)"],
                                                            "yellow_cards_against":table_epl[i]["SUM(team_yellow_cards_conceded_ft)"],
                                                            "red_cards":table_epl[i]["SUM(team_red_cards_recorded_ft)"],
                                                            "red_cards_against":table_epl[i]["SUM(team_red_cards_conceded_ft)"],
                                                            "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                            seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])

    #return render_template("stats_totals.html")
###########################

#######################
@app.route("/index_quiz", methods=["GET"])
def index_quiz():

    seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
    season = random.randint(2006,2022)
    teams_epl = db.execute("SELECT DISTINCT team_ft FROM EPLData WHERE season_ft = ?;",season)
    random_team = random.randint(1,20)
    table_epl = db.execute("select * FROM (select ROW_NUMBER() OVER(ORDER BY SUM(points_ft) DESC) place, team_ft, SUM(points_ft), SUM(win_ft), SUM(draw_ft), SUM(loss_ft), SUM(team_corners_recorded_ft), SUM(team_shots_recorded_ft), SUM(team_fouls_committed_recorded_ft), SUM(team_yellow_cards_recorded_ft), season_ft from EPLData where season_ft = ? GROUP BY team_ft ORDER BY SUM(points_ft) DESC) WHERE place=?;", season, random_team)
    answer = table_epl[0]["team_ft"]

    #return render_template("index_quiz.html", seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))])
    return render_template("index_quiz.html", stats_list=[{"team_ft": table_epl[i]["team_ft"],
                                                        "points": table_epl[i]["SUM(points_ft)"],
                                                        "wins": table_epl[i]["SUM(win_ft)"],
                                                        "draws": table_epl[i]["SUM(draw_ft)"],
                                                        "losses": table_epl[i]["SUM(loss_ft)"],
                                                        "corners_for": table_epl[i]["SUM(team_corners_recorded_ft)"],
                                                        "shots_for":table_epl[i]["SUM(team_shots_recorded_ft)"],
                                                        "fouls_commited":table_epl[i]["SUM(team_fouls_committed_recorded_ft)"],
                                                        "yellow_cards":table_epl[i]["SUM(team_yellow_cards_recorded_ft)"],
                                                        "season":table_epl[i]["season_ft"]} for i in range(0, len(table_epl))],
                                                        seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))],
                                                        teams_list=[{"team": teams_epl[i]["team_ft"]} for i in range(0, len(teams_epl))],
                                                        answer = answer)


"""
@app.route("/quiz", methods=["GET"])
def quiz():

    answer = request.form.get("input.value")

    if answer == '8':
        return render_template("correct.html")
    else:
        return render_template("incorrect.html")


    #check_answer = request.form.get("team")
    #if check_answer == None:
        season = 2022
        #if season == None:
        #   return apology()
        seasons_epl = db.execute("SELECT DISTINCT season_ft FROM EPLData ORDER BY season_ft;")
        teams_epl = db.execute("SELECT DISTINCT team_ft FROM EPLData;")
        random_team = random.randint(1,20)
        table_epl = db.execute("select * FROM (select ROW_NUMBER() OVER(ORDER BY SUM(points_ft) DESC) place, team_ft, SUM(points_ft), SUM(win_ft), SUM(draw_ft), SUM(loss_ft), SUM(team_corners_recorded_ft), SUM(team_shots_recorded_ft), SUM(team_fouls_committed_recorded_ft), SUM(team_yellow_cards_recorded_ft) from EPLData where season_ft = ? GROUP BY team_ft ORDER BY SUM(points_ft) DESC) WHERE place=?;", season, random_team)
        answer = table_epl[0]["team_ft"]

        return render_template("quiz.html", stats_list=[{"team_ft": table_epl[i]["team_ft"],
                                                        "points": table_epl[i]["SUM(points_ft)"],
                                                        "wins": table_epl[i]["SUM(win_ft)"],
                                                        "draws": table_epl[i]["SUM(draw_ft)"],
                                                        "losses": table_epl[i]["SUM(loss_ft)"],
                                                        "corners_for": table_epl[i]["SUM(team_corners_recorded_ft)"],
                                                        "shots_for":table_epl[i]["SUM(team_shots_recorded_ft)"],
                                                        "fouls_commited":table_epl[i]["SUM(team_fouls_committed_recorded_ft)"],
                                                        "yellow_cards":table_epl[i]["SUM(team_yellow_cards_recorded_ft)"]} for i in range(0, len(table_epl))],
                                                        seasons_list=[{"season": seasons_epl[i]["season_ft"]} for i in range(0, len(seasons_epl))],
                                                        teams_list=[{"team": teams_epl[i]["team_ft"]} for i in range(0, len(teams_epl))])
    #else:

"""
###########################

# me bo css
# me testu
# me shtu komente
# me dorzu

#conn.close()
#engine.dispose()

if __name__== '__main__':
    app.run(debug=true)

