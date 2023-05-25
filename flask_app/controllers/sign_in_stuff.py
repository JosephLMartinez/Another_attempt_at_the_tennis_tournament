from flask_app import app, Flask
from flask import render_template, redirect, session, request, flash
from flask_app.models.admin import Admin
from flask_app.models.player import Player
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#everyton starts here
@app.route("/")
def admin_index():
    # going back to first page automatically logs you out
    session['user']=False
    session['my_name']=False
    session['age']=False
    return render_template("first_page.html")

# preexisting users
@app.route("/sign_in")
def sign_in():
    # going to sign_in page automatically logs you out
    session['user']=False
    session['my_name']=False
    session['age']=False
    return render_template("sign_in.html")

# what kind of new user?
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

# new admin
@app.route("/new_admin")
def new_admin():
    return render_template("create_admin.html")

# new athlete
@app.route("/new_player")
def new_player():
    return render_template("create_player.html")

# adds tournament organizer to the system
@app.route("/create_admin", methods= ['POST'])
def create_admin():
    if not Admin.validate_admin(request.form):
        print("flash message")
        return redirect('/new_admin')
    admin_in_system= Admin.get_by_email(request.form['email'])
    if admin_in_system:
        flash('Account already exists please sign in')
        return redirect('/sign_in')
    data={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    admin=Admin.save(data)
    session['user']=admin
    admin_name=Admin.get_one(admin)
    session['my_name']=admin_name[0]['first_name']
    print(admin)
    return redirect("/admins")


# adds athlete to the system
@app.route("/create_player", methods= ['POST'])
def create_player():
    if not Player.validate_player(request.form):
        print("flash message")
        return redirect('/new_player')
    player_in_system= Player.get_by_email(request.form['email'])
    if player_in_system:
        flash('Account already exists please sign in')
        return redirect('/sign_in')
    data={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "age": request.form['age'],
        "email":request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    player=Player.save(data)
    session['user']=player
    player_name=Player.get_one(player)
    session['my_name']=player_name[0]['first_name']
    session['age']=player_name[0]['age']
    print(player)
    return redirect("/players")


# login for both
@app.route('/login', methods=['POST'])
def login():
    admin_in_system= Admin.get_by_email(request.form['email'])
    if not admin_in_system:
        player_in_system=Player.get_by_email(request.form['email'])
        if not player_in_system:
            flash('Invalid Email/Password')
            return redirect('/sign_in')
        if not bcrypt.check_password_hash(player_in_system.password, request.form['password']):
            flash("Invalid Email/Password")
            return redirect('/sign_in')
        player_name=Player.get_one(player_in_system.id)
        session['my_name']=player_name[0]['first_name']
        session['age']=player_name[0]['age']
        session['user']=player_in_system.id
        return redirect("/players")
    if not bcrypt.check_password_hash(admin_in_system.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    admin_name=Admin.get_one(admin_in_system.id)
    session['my_name']=admin_name[0]['first_name']
    session['user']= admin_in_system.id
    return redirect("/admins")


# logout
@app.route('/logout')
def logout():
    session['user']=False
    session['my_name']=False
    session['age']=False
    return redirect('/')

