from flask_app import app, Flask
from flask import render_template, redirect, session, request, flash
from flask_app.models.player import Player
from flask_app.models.admin import Admin
from flask_app.models.tournament import Tournament

# checks for existing tournaments and directs you there or if none starts you on making a new one
@app.route("/admins")
def admin_page():
    if not session['user']:
        return redirect('/')
    if not Admin.get_tournament(session['user']):
        return render_template("create_tournament.html")
    my_tournament=Admin.get_tournament(session['user'])
    tournament_players=Tournament.get_players(my_tournament[0]['id'])
    number_of_players=len(tournament_players)
    variable=1
    bracket_size=[1]
    while number_of_players>2*variable:
        variable=variable*2
        bracket_size.append(variable)
    print("before reverse:", bracket_size)
    bracket_size=list(reversed(bracket_size))
    print("bracket size:", bracket_size)
    round_one=bracket_size[0]
    return render_template("admin_tournament.html", tournament_players=tournament_players, bracket_size=bracket_size, round_one=round_one, number_of_players=number_of_players, my_tournament=my_tournament)

# it takes the info and sends it to tournaments table in SQL
@app.route("/new_tournament_available", methods=["POST"])
def make_a_tournament():
    if not session['user']:
        return redirect('/')
    if not Tournament.validate_tournament_posting(request.form):
        print("flash message")
        return redirect('/admins')
    data={
        "admin_id":session['user'],
        "tournament_name": request.form["tournament_name"],
        "state": request.form["state"],
        "city": request.form['city'],
        "low_age": request.form['low_age'],
        "high_age": request.form['high_age'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
    }
    Tournament.save(data)
    return redirect("/status")

# shows you the tournament you have
@app.route("/status")
def status():
    if not session['user']:
        return redirect('/')
    my_tournament=Admin.get_tournament(session['user'])
    tournament_players=Tournament.get_players(my_tournament[0]['id'])
    number_of_players=len(tournament_players)
    variable=1
    bracket_size=[1]
    while number_of_players>2*variable:
        variable=variable*2
        bracket_size.append(variable)
    print("before reverse:", bracket_size)
    bracket_size=list(reversed(bracket_size))
    print("bracket size:", bracket_size)
    round_one=bracket_size[0]
    return render_template("admin_tournament.html", tournament_players=tournament_players, bracket_size=bracket_size, round_one=round_one, number_of_players=number_of_players,my_tournament=my_tournament)

@app.route("/players")
def player_index():
    if not session['user']:
        return redirect('/')
    # checks to see if they are in a tournament if no they get to see tournaments
    if not Player.get_tournament_id(session['user']):
        session['age']=Player.get_age(session['user'])
        available_tournaments=Tournament.get_all(session['age'])
        return render_template("available_tournaments.html", available_tournaments=available_tournaments)
    # shows them their scheduled tournament
    my_tournament=Player.get_tournament_id(session['user'])
    tournament_players=Tournament.get_players(my_tournament)
    number_of_players=len(tournament_players)
    variable=1
    bracket_size=[1]
    while number_of_players>2*variable:
        variable=variable*2
        bracket_size.append(variable)
    print("before reverse:", bracket_size)
    bracket_size=list(reversed(bracket_size))
    print("bracket size:", bracket_size)
    round_one=bracket_size[0]
    return render_template("my_tournament.html", tournament_players=tournament_players, bracket_size=bracket_size, round_one=round_one, number_of_players=number_of_players)

# claims the tournament and shows you the bracket
@app.route("/claim_tournament/<int:num>")
def join_tournament(num):
    if not session['user']:
        return redirect('/')
    data={
        "id": session['user'],
        "tournament_id":num
    }
    # adds the tournament to the player
    Player.claim(data)
    # shows them their scheduled tournament
    my_tournament=Player.get_tournament_id(session['user'])
    tournament_players=Tournament.get_players(my_tournament)
    number_of_players=len(tournament_players)
    variable=1
    bracket_size=[1]
    while number_of_players>2*variable:
        variable=variable*2
        bracket_size.append(variable)
    print("before reverse:", bracket_size)
    bracket_size=list(reversed(bracket_size))
    print("bracket size:", bracket_size)
    round_one=bracket_size[0]
    return render_template("my_tournament.html", tournament_players=tournament_players, bracket_size=bracket_size, round_one=round_one, number_of_players=number_of_players)

# If you can no longer attend the tournament
@app.route("/leave_tournament")
def edit_appointment():
    if not session['user']:
        return redirect('/')
    Player.unclaim(session['user'])
    print("Age of player",session['age'])
    available_tournaments=Tournament.get_all(session['age'])
    print("available_tournaments", available_tournaments)
    return render_template("available_tournaments.html", available_tournaments=available_tournaments)

# by submitting the tournament you update the player score and delete the tournament (in that order)
@app.route("/submit_tournament", methods=["POST"])
def submit_tournament():
    if not session['user']:
        return redirect('/')
    my_tournament=Admin.get_tournament(session['user'])
    tournament_players=Tournament.get_players(my_tournament[0]['id'])
    number_of_players=len(tournament_players)
    variable=1
    bracket_size=[1]
    while number_of_players>2*variable:
        variable=variable*2
        bracket_size.append(variable)
    print("before reverse:", bracket_size)
    bracket_size=list(reversed(bracket_size))
    print("bracket size:", bracket_size)
    for round in bracket_size:
            for each in range(round):
                tournament_player=request.form[f"victor{each}"]
                if not Tournament.validate_tournament_score(tournament_player):
                    print("flash message")
                    return redirect("/admins")
                # this looks redundant but is necessary to avoid adding points to a player's score before a validation fail occurs. That would give player extra points they didn't earn upon a successful touornament submission 
            for each in range(round):
                tournament_player= request.form[f"victor{each}"]
                Player.add_a_point(tournament_players[int(tournament_player)]['id'])
    data={
        "admin_id":session['user'],
        "tournament_id": Player.get_tournament_id(tournament_players[0]['id'])
    }
    Tournament.delete(data)
    return redirect("/admins")
    












