from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX= re.compile(r'^[a-zA-A0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Player:
    schema="tennis_tournament_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.age=data['age']
        self.score=data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_player(player):
        is_valid=True
        if len(player['first_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(player['first_name']) < 3:
            flash('First name must be atleast 3 characters long.')
            is_valid=False
        if len(player['last_name']) < 1:
            flash('Last name cannot be blank.')
            is_valid=False
        elif len(player['last_name']) < 3:
            flash('Last name must be atleast 3 characters long.')
            is_valid=False
        if len(player['email'])<1:
            flash('Email cannot be blank')
            is_valid=False
        elif len(player['email']) < 8:
            flash('Email must be atleast 8 characters long')
            is_valid=False
        elif not EMAIL_REGEX.match(player['email']):
            flash('Invalid email format')
            is_valid=False
        if len(player['password']) < 1:
            flash('Password cannot be blank.')
            is_valid=False
        elif len(player['password']) < 8:
            flash('Password must be atleast 8 characters long.')
            is_valid=False
        if len(player['confirm_password']) < 1:
            flash('Please confirm your password.')
            is_valid=False
        elif player['password']!=player['confirm_password']:
            flash("Your passwords do not match.")
            is_valid=False
        if not player['age']:
            flash("Don't forget to select your age.")
            is_valid=False
        return is_valid

    # CREATE
    @classmethod
    def save(cls,data):
        query= "INSERT INTO players (first_name, last_name, email, password, age, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(age)s, NOW(), NOW() );"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    #Do they exist?
    @classmethod
    def get_by_email(cls,email):
        query= "SELECT * FROM players WHERE email = %(email)s;"
        results=connectToMySQL(cls.schema).query_db(query, {"email":email})
        if len(results)<1:
            return False
        return cls(results[0])

    # Read
    @classmethod
    def get_one(cls,id):
        query = "SELECT * FROM players WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        players = []
        for player in results:
            players.append( player )
        return players
    
    # finding their tournament id
    @classmethod
    def get_tournament_id(cls,id):
        query = "SELECT tournament_id FROM players WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        if not results[0]['tournament_id']:
            return False
        return results[0]['tournament_id']

    # UPDATE to claim
    @classmethod
    def claim(cls, data):
        query="UPDATE players SET tournament_id= %(tournament_id)s, updated_at=NOW() WHERE id=%(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)
        return
    
    # Updates to unclaim
    @classmethod
    def unclaim(cls,id):
        query="UPDATE players SET tournament_id= NULL, updated_at=NOW() WHERE id=%(id)s;"
        connectToMySQL(cls.schema).query_db(query, {"id":id})
        return
        
    # get player age
    @classmethod
    def get_age(cls,id):
        query = "SELECT age FROM players WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        # players = []
        # for player in results:
        #     players.append( player )
        print (results)
        return results[0]['age']
    
    # adds a point to the winning player
    @classmethod
    def add_a_point(cls,id):
        query="UPDATE players SET score=score+1, updated_at=NOW() WHERE id=%(id)s;"
        connectToMySQL(cls.schema).query_db(query, {"id":id})
        return