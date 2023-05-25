from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX= re.compile(r'^[a-zA-A0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Admin:
    schema="tennis_tournament_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #Validate New Admin
    @staticmethod
    def validate_admin(admin):
        is_valid=True
        if len(admin['first_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(admin['first_name']) < 3:
            flash('First name must be atleast 3 characters long.')
            is_valid=False
        if len(admin['last_name']) < 1:
            flash('Last name cannot be blank.')
            is_valid=False
        elif len(admin['last_name']) < 3:
            flash('Last name must be atleast 3 characters long.')
            is_valid=False
        if len(admin['email'])<1:
            flash('Email cannot be blank')
            is_valid=False
        elif len(admin['email']) < 8:
            flash('Email must be atleast 8 characters long')
            is_valid=False
        elif not EMAIL_REGEX.match(admin['email']):
            flash('Invalid email format')
            is_valid=False
        if len(admin['password']) < 1:
            flash('Password cannot be blank.')
            is_valid=False
        elif len(admin['password']) < 8:
            flash('Password must be atleast 8 characters long.')
            is_valid=False
        if len(admin['confirm_password']) < 1:
            flash('Please confirm your password.')
            is_valid=False
        elif admin['password']!=admin['confirm_password']:
            flash("Your passwords do not match.")
            is_valid=False
        return is_valid

    # CREATE
    @classmethod
    def save(cls,data):
        query= "INSERT INTO admins (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    #Do they exist?
    @classmethod
    def get_by_email(cls,email):
        query= "SELECT * FROM admins WHERE email = %(email)s;"
        results=connectToMySQL(cls.schema).query_db(query, {"email":email})
        if len(results)<1:
            return False
        return cls(results[0])
    
    # Read
    @classmethod
    def get_one(cls,id):
        query = "SELECT first_name FROM admins WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        admins = []
        for admin in results:
            admins.append( admin )
        return admins
    

    # READ one for admins showing their tournament
    @classmethod
    def get_tournament(cls, id):
        query= "SELECT * FROM tournaments WHERE admin_id= %(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, {"id":id})
        print("Get tournament results",results)
        if not results:
            return False
        return results
    
