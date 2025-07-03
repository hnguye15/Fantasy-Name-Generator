#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session, redirect, url_for
from flask_restful import reqparse, Resource, Api
from flask_session import Session
from email_validator import validate_email, EmailNotValidError
import json
import ssl

from db_util import *
import pymysql
import settings # Server and database settings, stored in settings.py

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################
###ERROR HANDLERS###
####################################################################################
@app.errorhandler(400) # Bad request error
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(403) # Bad request error
def not_found(error):
	return make_response(jsonify( { 'status': 'Access denied' } ), 403)

@app.errorhandler(404) # Resource not found error
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

@app.errorhandler(409) # Resource not found error
def not_found(error):
	return make_response(jsonify( { 'status': 'Object already exists' } ), 409)

@app.errorhandler(401) # Resource not found error
def not_found(error):
	return make_response(jsonify( { 'status': 'Authentication Failed' } ), 401)
####################################################################################




#########################
###VALIDATOR FUNCTIONS###
####################################################################################
def validateAlphanumeric(string):
	for char in string:
		if ord(char) < 32 or (32 < ord(char) < 40) or (41 < ord(char) < 48) or (57 < ord(char) < 65) or (90 < ord(char) < 97) or ord(char) > 122:
			print("String must not contain any special characters!")
			return False
			
	return True;

def validateUsername(username):
	if len(username) < 8:
		print("Username is too short!")
		return False
		
	if len(username) > 50:
		print("Username is too long!")
		return False
		
	for char in username:
		if ord(char) < 48 or (57 < ord(char) < 65) or (90 < ord(char) < 97) or ord(char) > 122:
			print("Username must not contain any special characters!")
			return False
			
	return True;
	
def validatePassword(password):
	if len(password) < 8:
		print("Password is too short!")
		return False
	if len(password) > 64:
		print("Password is too long!")
		return False
		
	hasLowercase = False
	hasUppercase = False
	hasDigit = False
	hasSpecial = False
	hasInsecureSpecial = False
	
	for char in password:
		if (96 < ord(char) < 123):
			hasLowercase = True
		elif (64 < ord(char) < 91):
			hasUppercase = True
		elif (47 < ord(char) < 58):
			hasDigit = True
		elif (char in '@.#$!%^&*.?'):
			hasSpecial = True
		else:
			hasInsecureSpecial = True
			
	if (hasLowercase == True) and (hasUppercase == True) and (hasDigit == True) and (hasSpecial == True) and (hasInsecureSpecial == False):
		return True
	else:
		print("Password is not strong enough!");
		return False

# Using email-validator from https://pypi.org/project/email-validator/
def validateEmail(email):
	try:
		check = validate_email(email)
		email = check.normalized
		return True
	except EmailNotValidError as e:
		print(str(e))
		return False
####################################################################################




###############
###REROUTERS###
####################################################################################
@app.route('/')
def landing():
	return redirect('static/index.html')

@app.route('/static')
def index():
	return redirect('static/index.html')
####################################################################################




###########################
###RESTFUL API ENDPOINTS###
####################################################################################
class SignIn(Resource):
	
	#POST: Set Session and return Cookie
	def post(self):

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		#Validate input
		if (validateUsername(request_params['username']) == False) or (validatePassword(request_params['password']) == False):
			response = {'status': 'Access denied'}
			responseCode = 403
			return make_response(jsonify(response, responseCode))
		
		#If username is already in the session, auto accept
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				sqlProc = 'getUserByUsernameAndPassword'
				sqlArgs = [request_params['username'], request_params['password']]
				
				#Authenticate
				if db_access(sqlProc, sqlArgs) != ():
					session['username'] = request_params['username']
					response = {'status': 'success' }
					responseCode = 200
				else:
					response = {'status': 'Access denied'}
					responseCode = 403
			except Exception as e:
				abort(500, message = e) # Server Error

		return make_response(jsonify(response, responseCode))

	# GET: Check Cookie data with Session data
	def get(self):
		success = False
		if ('username' in session) and validateUsername('username'):
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'failed'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

class SignOut(Resource):
	
	# DELETE: Remove user from session
	def delete(self):
		
		#Validate credentials
		if ('username' in session) and validateUsername('username'):
			session.pop('username')
			response = {'status': 'success'}
			responseCode = 204
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

class Register(Resource):
	
	#POST: Register a new user
	def post(self):

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			parser.add_argument('email', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		#Validate input
		if (validateUsername(request_params['username']) == False) or (validatePassword(request_params['password']) == False) or (validateEmail(request_params['email']) == False):
			response = {'status': 'Access denied'}
			responseCode = 403
			return make_response(jsonify(response, responseCode))
		
		#If username is already in the session, auto accept
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				sqlProc = 'addUser'
				sqlArgs = [[request_params['username']], request_params['password'], request_params['email']]
				
				#Authenticate
				if db_access('getUserByUsername', request_params['username']) != ():
					db_access(sqlProc, sqlArgs)
					session['username'] = request_params['username']
					response = {'status': 'success' }
					responseCode = 200
				else:
					response = {'status': 'Access denied'}
					responseCode = 403
			except Exception as e:
				abort(500, message = e) # Server Error

		return make_response(jsonify(response, responseCode))

class Password(Resource):
	
	#POST: Change the user's password
	def post(self, username):

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('oldPassword', type=str, required=True)
			parser.add_argument('newPassword', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		#Validate input
		if (validateUsername(request_params['username']) == False) or (validatePassword(request_params['oldPassword']) == False) or (validatePassword(request_params['newPassword']) == False):
			response = {'status': 'Access denied'}
			responseCode = 403
			return make_response(jsonify(response, responseCode))

		try:
			sqlProc = 'changePasswordByUsernameAndPassword'
			sqlArgs = [[request_params['username']], request_params['oldPassword'], request_params['newPassword']]
			#Authenticate
			if db_access('getUserByUsernameAndPassword', [request_params['username'], request_params['oldPassword']]) != ():
				print(db_access('getUserByUsernameAndPassword', [request_params['username'], request_params['oldPassword']]))
				db_access(sqlProc, sqlArgs)
				response = {'status': 'success' }
				responseCode = 200
			else:
				response = {'status': 'Access denied'}
				responseCode = 403
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response, responseCode))

class Feedback(Resource):
	
	# POST: Add a feedback to the database
	def post(self, username):
		
		#If the user is not logged in, don't continue
		if ('username' not in session) or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "feedback" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		feedback = request.json['feedback']

		sqlProc = 'saveFeedback'
		sqlArgs = [username, feedback]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Get feedback from the database
	def get(self, username):
		
		#If the user is not logged in, don't continue
		if 'username' not in session or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)
		
		sqlProc = 'getFeedback'
		
		try:
			rows = db_access(sqlProc, '')
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error
		
		print(rows)
		return make_response(jsonify({'feedbacks': rows}), 201) # turn set into json and return it

	# DELETE: Delete feedback by username
	def delete(self, username):
		
		#If the user is not logged in, don't continue
		if 'username' not in session or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)
			
		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)
		
		username = request.json['username']
		
		#Validate input
		if validateAlphanumeric(username) == False:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'deleteFeedbackByUser'
		sqlArgs = username
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Item deleted'}
			responseCode = 204
		except Exception as e:
			abort(500, message = e) # server error
		return make_response(jsonify(response, responseCode))

class FirstName(Resource):
	
	# POST: Add a first name to the database
	def post(self):
		
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']
		
		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'addFirstName'
		sqlArgs = [name, gender, background]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except pymysql.IntegrityError as e:
			response = {'status': 'duplicate entry'}
			responseCode = 409
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Generate a random first name from the database
	def get(self):
		
		#If the submitted data is not valid for the desired function, do not continue
		if not "gender" in request.args or not "background" in request.args:
			response = {'status': 'invalid input, bad input parameter'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		count = 0
		if ("count" not in request.args):
			count = 1
		else:
			count = request.args.get("count")
		gender = request.args.get('gender')
		background = request.args.get('background')
		
		#Validate input
		if (validateAlphanumeric(count) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'genFirstName'
		sqlArgs = [gender, background, count]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify({'names': rows}), 201) # turn set into json and return it

	# DELETE: Delete a first name from the database
	def delete(self):
		
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']
		
		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'removeFirstNameByInfo'
		sqlArgs = [name, gender, background]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Item deleted'}
			responseCode = 204
		except Exception as e:
			abort(500, message = e) # server error
		return make_response(jsonify(response, responseCode))

class MiddleName(Resource):
	
	# POST: Add a middle name to the database
	def post(self):
		
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateAlphanumeric(background) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']

		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'addMiddleName'
		sqlArgs = [name, gender, background]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except pymysql.IntegrityError as e:
			response = {'status': 'duplicate entry'}
			responseCode = 409
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Generate a random middle name from the database
	def get(self):
		
		#If the submitted data is not valid for the desired function, do not continue
		if not "gender" in request.args or not "background" in request.args:
			response = {'status': 'invalid input, bad input parameter'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		count = 0
		if ("count" not in request.args):
			count = 1
		else:
			count = request.args.get("count")
		gender = request.args.get('gender')
		background = request.args.get('background')
		
		#Validate input
		if (validateAlphanumeric(count) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'genMiddleName'
		sqlArgs = [gender, background, count]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify({"names": rows}), 201) # turn set into json and return it

	# DELETE: Delete a middle name from the database
	def delete(self):
		
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateAlphanumeric(background) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']

		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'removeMiddleNameByInfo'
		sqlArgs = [name, gender, background]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Item deleted'}
			responseCode = 204
		except Exception as e:
			abort(500, message = e) # server error
		return make_response(jsonify(response, responseCode))

class LastName(Resource):
	
	# POST: Add a middle name to the database
	def post(self):
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateAlphanumeric(background) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		elif not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']
		
		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'addLastName'
		sqlArgs = [name, gender, background]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except pymysql.IntegrityError as e:
			response = {'status': 'duplicate entry'}
			responseCode = 409
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Generate a random last name from the database
	def get(self):
		
		#If the submitted data is not valid for the desired function, do not continue
		if not "gender" in request.args or not "background" in request.args:
			response = {'status': 'invalid input, bad input parameter'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		count = 0
		if ("count" not in request.args):
			count = 1
		else:
			count = request.args.get("count")
		gender = request.args.get('gender')
		background = request.args.get('background')
		
		#Validate input
		if (validateAlphanumeric(count) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)
		
		sqlProc = 'genLastName'
		sqlArgs = [gender, background, count]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify({'names': rows}), 201) # turn set into json and return it

	# DELETE: Delete a last name from the database
	def delete(self):
		
		#If the user is not logged in, don't continue
		#If the user is not an admin, don't continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateAlphanumeric(background) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']

		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'removeLastNameByInfo'
		sqlArgs = [name, gender, background]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Item deleted'}
			responseCode = 204
		except Exception as e:
			abort(500, message = e) # server error
		return make_response(jsonify(response, responseCode))

class SavedNames(Resource):
	
	# POST: Add a full name to the database of user saved names
	def post(self, username):
		
		#If the user is not logged in, don't continue
		if ('username' not in session) or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json or not "gender" in request.json or not "background" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		name = request.json['name']
		gender = request.json['gender']
		background = request.json['background']

		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(gender) == False) or (validateAlphanumeric(background) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'saveName'
		sqlArgs = [username, name, gender, background]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except pymysql.IntegrityError as e:
			response = {'status': 'duplicate entry'}
			responseCode = 409
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Get saved names for a specific user from the database
	def get(self, username):
		
		#If the user is not logged in, don't continue
		if 'username' not in session or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		count = 1
		if ("count" not in request.args):
			count = 10
		else:
			count = request.args.get("count")
		
		#Validate input
		if (validateAlphanumeric(count) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'getNames'
		sqlArgs = [username, count]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 201
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify({'names': rows}), 201) # turn set into json and return it

	# DELETE: Delete a saved name from the database
	def delete(self, username):
		
		#If the user is not logged in, don't continue
		if 'username' not in session or (validateUsername('username') == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the accessing user is not the owner or an admin, do not allow
		if (session['username'] != username) and (checkAdmin(session['username']) == 0) and (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)
			
		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "name" in request.json:
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)
		
		name = request.json['name']
		confirmDeleteAll = request.json['confirmDeleteAll']
		
		#Validate input
		if (validateAlphanumeric(name) == False) or (validateAlphanumeric(confirmDeleteAll) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'deleteNameByUser'
		sqlArgs = [username, name, confirmDeleteAll]
		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Item deleted'}
			responseCode = 204
		except Exception as e:
			abort(500, message = e) # server error
		return make_response(jsonify(response, responseCode))

class AdminControl(Resource):
	
	# POST: Mark a user as an admin
	def post(self):
		
		#If the user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		userID = request.json['username']
		
		#Validate input
		if (validateAlphanumeric(userID) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		if(checkUser(userID) == 0):
			response = {'status': 'User does not exist'}
			responseCode = 404
			return make_response(jsonify(response), responseCode)

		sqlProc = 'addAdminByUsername'
		sqlArgs = [userID]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 200
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)


	# GET: Check if a user is an admin
	def get(self):
		
		#If the user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		userID = request.args.get('username')
		
		#Validate input
		if (validateAlphanumeric(userID) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		if(checkUser(userID) == 0):
			response = {'status': 'User does not exist'}
			responseCode = 404
			return make_response(jsonify(response), responseCode)

		sqlProc = 'getAdminByUsername'
		sqlArgs = [userID]

		try:
			rows = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(500, message = e) # Server Error

		if(len(rows) < 1):
			response = {'status': 'Use is not an admin'}
			responseCode = 400
		else:
			response = {'status': 'User is an admin'}
			responseCode = 200

		return make_response(jsonify(response), responseCode)

	# DELETE: Mark a user as no longer an admin
	def delete(self):
		
		#If the user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		userID = request.json['username']
		
		#Validate input
		if (validateAlphanumeric(userID) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		if(checkUser(userID) == 0):
			response = {'status': 'User does not exist'}
			responseCode = 404
			return make_response(jsonify(response), responseCode)

		sqlProc = 'deleteAdminByUsername'
		sqlArgs = [userID]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'Admin removed'}
			responseCode = 400
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

class UserControl(Resource):
	
	# POST: Create a user when you are not logging in as that user
	def post(self):
		
		#If the user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		userID = request.json['username']
		
		#Validate input
		if (validateAlphanumeric(userID) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'addUser'
		sqlArgs = [userID]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 200
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)

	# GET: Check if a user exists
	def get(self):
		
		#If the accessing user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		username = request.args.get('username')
		
		#Validate input
		if (validateAlphanumeric(username) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'getUserByUsername'
		sqlArgs = [username]

		try:
			rows = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(500, message = e) # Server Error

		if(len(rows) < 1):
			response = {'status': 'Name is not associated with a user'}
			responseCode = 400
		else:
			response = {'status': 'Name is a user'}
			responseCode = 200

		return make_response(jsonify(response), responseCode)

	# DELETE: Delete a user from the database
	def delete(self):
		
		#If the user is not logged in and isn't an admin, do not continue
		if ('username' not in session) or (checkAdmin(session['username']) == 0) or (validateUsername(session['username']) == False):
			response = {'status': 'Authentication Failed'}
			responseCode = 401
			return make_response(jsonify(response), responseCode)

		#If the submitted data is not valid for the desired function, do not continue
		if not request.json or not "username" in request.json:
			response = {'status': 'invalid ID supplied'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		userID = request.json['username']
		
		#Validate input
		if (validateAlphanumeric(userID) == False):
			response = {'status': 'invalid input, object invalid'}
			responseCode = 400
			return make_response(jsonify(response), responseCode)

		sqlProc = 'deleteUserByUsername'
		sqlArgs = [userID]

		try:
			rows = db_access(sqlProc, sqlArgs)
			response = {'status': 'success'}
			responseCode = 200
		except Exception as e:
			abort(500, message = e) # Server Error

		return make_response(jsonify(response), responseCode)
####################################################################################




######################
###ENDPOINT OBJECTS###
####################################################################################
api = Api(app)
api.add_resource(SignIn, '/login')
api.add_resource(SignOut, '/logout')
api.add_resource(Register, '/register')
api.add_resource(FirstName, '/first-name')
api.add_resource(MiddleName, '/middle-name')
api.add_resource(LastName, '/last-name')
api.add_resource(SavedNames, '/user/<string:username>/saved-names')
api.add_resource(Password, '/user/<string:username>/password')
api.add_resource(Feedback, '/user/<string:username>/feedback')
api.add_resource(AdminControl, '/admin')
api.add_resource(UserControl, '/user')
#############################################################################




####################
###RUN THE SERVER###
####################################################################################
if __name__ == "__main__":
	# Certificate is generated by running the makeCert.sh script
	context = ('cert.pem', 'key.pem')
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG
	)