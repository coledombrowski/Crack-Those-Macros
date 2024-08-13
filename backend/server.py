from flask import Flask, request, session ,jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from dotenv import load_dotenv
from flask_cors import CORS
from mealSuggestion import get_meal_recommendation, get_muscle_gain_meal
import pyodbc 
import pandas as pd 
import os
import json

# App Initialization
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = False
CORS(app, supports_credentials=True)
# Database Initialization
load_dotenv()
db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_driver = os.getenv('DB_DRIVER') or '{SQL Server}'
db_conn_str = f'DRIVER={db_driver};SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}' 

# User Login Initialization
login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
	pass

# App - Home Page
@app.route("/")
def home_page():
	return

# App - Account Creation Page
@app.route("/register-account", methods=['POST'])
def account_creation_page():
	error_message = ''
	hasCreatedUser = False

	username = request.json['username']
	password = request.json['password']

	# Check if User already exists
	db_connection = pyodbc.connect(db_conn_str)
	cursor = db_connection.cursor()
	query = f"SELECT COUNT(*) FROM [dbo].[Users] WHERE Username = '{username}'"
	cursor.execute(query)
	count = cursor.fetchone()[0]
	
	if (count != 0):
		error_message = 'An account could not be created - Try a unique Username'

	# Create the new User
	else:
		new_user = {
			'username': username,
			'password': password
		}
		sql_command = f"""
			INSERT INTO [dbo].[Users] (Username, Password, Is_First_Login)
			VALUES ('{username}', '{password}', 1)
		"""
		cursor.execute(sql_command)
		hasCreatedUser = True
	
	# Commit the changes and close the connection 
	db_connection.commit() 
	cursor.close() 
	db_connection.close()

	# Send Response
	if (hasCreatedUser):
		return {
			"result": "Success",
			"message": "An account has been created"
		}, 200
	else:
		return {
			"result": "Failed",
			"message": error_message
		}, 400
		
# App - Login Page
@app.route("/login-user", methods=['POST'])
def login_page():
	if current_user.is_active:
		return {
			"result": "Failed",
			"message": "Error - User is already logged in"
		}, 400
	
	username = request.json['username']
	password = request.json['password']

	# Check for User Credentials
	db_connection = pyodbc.connect(db_conn_str)
	query = f"SELECT * FROM [dbo].[Users] WHERE Username = '{username}'"
	user_result = pd.read_sql_query(query, db_connection)
	# Commit the changes and close the connection
	db_connection.close()
	
	# Send Response
	if (not user_result.empty) and (user_result['Password'][0] == password):
		user = User()
		user.id = username
		login_user(user)

		# Add goal to user if present
		if 'Goal' in user_result:
			session['goal_choice'] = user_result['Goal'][0]
		else:
			session['goal_choice'] = 0
		
		
		return {
			"username": user.id
		}, 200
	
	else:
		return {
			"result": "Failed",
			"message": "Account details are invalid"
		}, 401
		
# App - Logout Page
@app.route('/logout-user')  
def logout_page():  
	if current_user.is_active:
		session['goal_choice'] = 0
		logout_user()  
		return {
			"result": "Success",
			"message": "Logged out successfully"
		}, 200
		
	else:
		return {
			"result": "Failed",
			"message": "Error - You are not logged in"
		}, 500
# App - Saving data from Questionnaire
@app.route('/questionnaire', methods=['POST'])
def update_questionnaire():
	data = request.get_json()
	user_questionnaire = {
		"goal": data['goal'],
		"goalWeightChange": data['goalWeightChange'],
		"gender": data['gender'],
		"age": int(data['age']),
		"height_ft": int(data['height_ft']),
		"height_in": int(data['height_in']),
		"weight_lb": int(data['weight_lb']),
		"muscle_gain": float(data['muscle_gain'])
	}
	db_connection = pyodbc.connect(db_conn_str)
	cursor = db_connection.cursor()
	query = f"SELECT * FROM [dbo].[Users] WHERE Username = '{current_user.id}'"
	result = pd.read_sql_query(query, db_connection)
	# print("Current user data before update:")
	# print(result)
	update_query = f"""
        UPDATE [dbo].[Users]
        SET
            Goal = ?,
            Goal_Pound = ?,
            Gender = ?,
            Age = ?,
            Height_ft = ?,
            Height_in = ?,
            Weight = ?,
            Goal_Muscle = ?
        WHERE
            Username = ?
        """
	cursor.execute(update_query, (
            user_questionnaire["goal"],
            user_questionnaire["goalWeightChange"],
            user_questionnaire["gender"],
            user_questionnaire["age"],
            user_questionnaire["height_ft"],
            user_questionnaire["height_in"],
            user_questionnaire["weight_lb"],
            user_questionnaire["muscle_gain"],
            current_user.id
        ))
	db_connection.commit()
	#print("User table after updating")
	result = pd.read_sql_query(query, db_connection)
	print(result)
	cursor.close()
	db_connection.close()
	
	return jsonify({"message": "User data save successfully"}),200

# App - Get User Profile information from Database
@app.route('/api/get-user-profile')
def get_user_profile():
	# Get User Profile
	db_connection = pyodbc.connect(db_conn_str)
	query = f"SELECT * FROM [dbo].[Users] WHERE Username = '{current_user.id}'"
	result = pd.read_sql_query(query, db_connection)
	# Commit the changes and close the connection
	db_connection.close()

	# Set Variables
	username = str(result['Username'][0])
	height_ft = str(result['Height_ft'][0])
	height_in = str(result['Height_in'][0])
	weight = str(result['Weight'][0])
	goal = result['Goal'][0]

	# Cache variables to Session
	
	session['height_ft'] = height_ft
	session['height_in'] = height_in
	session['current_weight'] = weight
	session['goal_choice'] = goal
	
	return {
		"userProfileData": {
			"name": current_user.id,
			"heightFeet": height_ft,
			"heightInches": height_in,
			"weight": weight,
			"goal": goal
		}
	}, 200

# App - Get User Goal information from Database
@app.route('/api/get-user-goals')
def get_user_goals():
	# Get Goals
	db_connection = pyodbc.connect(db_conn_str)
	query = f"SELECT * FROM [dbo].[v_UserGoals] WHERE Username = '{current_user.id}'"
	result = pd.read_sql_query(query, db_connection)
	# Commit the changes and close the connection
	db_connection.close()
	
	# Set primary User Goal Values
	goal = result['Goal'][0]
	user_weight = int(result['Weight'][0])

	if "muscle" in goal.lower():
		# Cache variables to Session
		session['muscle_gain_goal'] = 5

	else:
		# Set weight related variables
		goal_pound = int(result['Goal_Pound'][0])
		weight_difference = user_weight - goal_pound

		if (user_weight <= 99):
			weight_choice = "0-99 lb"
		elif (100 <= user_weight) and (user_weight <= 150):
			weight_choice = "100-150 lb"
		elif (151 <= user_weight) and (user_weight <= 200):
			weight_choice = "151-200 lb"
		elif (201 <= user_weight) and (user_weight <= 250):
			weight_choice = "201-250 lb"
		else:
			weight_choice = "251-300 lb"

		if (goal == "Lose weight") and (weight_difference <= 5):
			pounds_choice = 5
			amount_choice = 'A little weight'
		elif (goal == "Lose weight") and (weight_difference > 5):
			pounds_choice = 10
			amount_choice = 'More weight'
		elif (goal == "Gain weight") and (weight_difference <= 15):
			pounds_choice = 15
			amount_choice = 'A little weight'
		elif (goal == "Gain weight") and (weight_difference > 15):
			pounds_choice = 20
			amount_choice = 'More weight'
		else:
			amount_choice = "More weight"
			pounds_choice = 0

		# Cache variables to Session
		session['amount_choice'] = amount_choice
		session['pounds_choice'] = pounds_choice
		session['weight_choice'] = weight_choice

	# Cache general variables to Session
	session['goal_choice'] = goal
	session['current_weight'] = user_weight

	return {
		"goal": goal
	}, 200

# App - Get Meal Suggestion
@app.route('/api/get-meal-suggestion', methods=['POST'])
def get_meal_suggestion():
	meal_time_choice = request.json['mealTimeChoice']
	session['meal_time_choice'] = meal_time_choice

	recommendation = get_meal_recommendation(str(current_user.id),session['goal_choice'], session['amount_choice'], session['pounds_choice'], session['weight_choice'], session['meal_time_choice'])
	
	# Cache current meal recommendation
	session['recommendation'] = {
		"recommendation": {
			"meal": recommendation
		}
	}

	return session['recommendation'], 200

# App - Get Meal Suggestion for Protein
@app.route('/api/get-meal-suggestion/protein', methods=['POST'])
def get_protein_meal_suggestion():
	meal_time_choice = request.json['mealTimeChoice']
	session['meal_time_choice'] = meal_time_choice

	recommendation = get_muscle_gain_meal(str(current_user.id),session['current_weight'], session['muscle_gain_goal'])

	# Cache current meal recommendation
	session['recommendation'] = {
		"recommendation": recommendation
	}
	
	return session['recommendation'], 200

# App - Get User Login Status
@app.route('/get-current-user-state')  
def get_current_user_state():
	if current_user.is_active:
		return {
			"result": "True",
			"username": current_user.id,
			"goal": session['goal_choice']
		}, 200
	else:
		return {
			"result": "False"
		}, 200

# App - Get Session aka Cache values
@app.route('/api/session')
def get_session_object():
	return {
		"session": session
	}

# Flask-Login Helper
@login_manager.user_loader  
def user_loader(username):  
	user = User()  
	user.id = username
	return user
@login_manager.user_loader
def load_user(user_id):
    
    db_connection = pyodbc.connect(db_conn_str)
    query = f"SELECT * FROM [dbo].[Users] WHERE Username = '{user_id}'"
    user_result = pd.read_sql_query(query, db_connection)
    db_connection.close()
    
    if not user_result.empty:
        user = User()
        user.id = user_id
        return user
    return None

# Run Server
if __name__ == '__main__':
	app.run(debug=True)
