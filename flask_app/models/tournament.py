from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Tournament:
    schema="tennis_tournament_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.tournament_name = data['tournament_name']
        self.state=data['state']
        self.city=data['city']
        self.low_age=data['low_age']
        self.high_age=data['high_age']
        self.start_date = data['start_date']
        self.end_date = data ['end_date']
        self.admin_id=['admin_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE
    @classmethod
    def save(cls,data):
        query= "INSERT INTO tournaments (admin_id, tournament_name, state, city, low_age, high_age, start_date, end_date, created_at, updated_at) VALUES (%(admin_id)s, %(tournament_name)s, %(state)s, %(city)s, %(low_age)s, %(high_age)s, %(start_date)s, %(end_date)s, NOW(), NOW() );"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    # validate the tournament
    @staticmethod
    def validate_tournament_posting(tournament_posting):
        is_valid=True
        if len(tournament_posting['tournament_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(tournament_posting['tournament_name']) < 5:
            flash("The Dog's name must be atleast 5 characters long.")
            is_valid=False
        if not tournament_posting['state']:
            flash('Pick a state')
            is_valid=False
        if not tournament_posting['city']:
            flash('Pick a city')
            is_valid=False
        if not tournament_posting['low_age']:
            flash('Select the low range of age for the participants')
            is_valid=False
        if not tournament_posting['high_age']:
            flash('Select the high range of age for the participants')
            is_valid=False
        if not tournament_posting['start_date']:
            flash('Invalid start date')
            is_valid=False
        if not tournament_posting['end_date']:
            flash('Invalid end date')
            is_valid=False
        return is_valid

    # READ All that fit age
    @classmethod
    def get_all(cls,age):
        query = "SELECT id,tournament_name, state, city, low_age, high_age, DATE_FORMAT(start_date, '%M %d %Y'), DATE_FORMAT(end_date, '%M %d %Y') FROM tournaments;"
        results = connectToMySQL(cls.schema).query_db(query)
        data=[]
        for row  in results:
            this={
                "id": row["id"],
                "tournament_name": row["tournament_name"],
                "state": row["state"],
                "city": row["city"],
                "low_age": row["low_age"],
                "high_age": row["high_age"],
                "start_date": row["DATE_FORMAT(start_date, '%M %d %Y')"],
                "end_date": row["DATE_FORMAT(end_date, '%M %d %Y')"]
            }
            print(this)
            if age<= this['high_age']:
                if age>= this["low_age"]:
                    data.append(this)
            print(data)
        return data
    
    # This will get all the players that are in the tournament
    @classmethod
    def get_players(cls,id):
        query= "SELECT players.id, first_name, last_name, age, score,admin_id,tournament_name FROM players JOIN tournaments ON tournaments.id=players.tournament_id WHERE tournament_id= %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        players = []
        for player in results:
            players.append( player )
        return players
    
    # DELETE
    @classmethod
    def delete(cls,data):
        query= "UPDATE players SET tournament_id=NULL WHERE tournament_id= %(tournament_id)s;"
        connectToMySQL(cls.schema).query_db(query, data)
        query= "DELETE FROM tournaments WHERE admin_id= %(admin_id)s;"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    # validate the tournament
    @staticmethod
    def validate_tournament_score(tournament_posting):
        is_valid=True
        if tournament_posting=="-1":
            flash("Each round must have it's champions")
        return is_valid

















    









    # this will be used to get the players
    # READ All of MINE
    @classmethod
    def get_all_of_mine(cls,id):
        query = "SELECT id,tournament_name,player_id, admin_id,  DATE_FORMAT(start_date, '%M %d %Y'), DATE_FORMAT(end_date, '%M %d %Y'), finished FROM tournaments;"
        results = connectToMySQL(cls.schema).query_db(query)
        data=[]
        for row  in results:
            this={
                "id": row["id"],
                "player_id": row["player_id"],
                "tournament_name": row["tournament_name"],
                "start_date": row["DATE_FORMAT(start_date, '%M %d %Y')"],
                "end_date": row["DATE_FORMAT(end_date, '%M %d %Y')"],
                "admin_id": row["admin_id"]
            }
            if this['player_id']==id:
                data.append(this)
                print(data)
        return data